"""Small offline keyword index for curated ColiDev course materials.

Only Markdown under 02_Areas and Markdown/text cheat sheets under
03_Resources/Cheatsheets are indexed. Prompts, plans, dotfiles, symlinks,
and files outside those roots are intentionally excluded.
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import logging
import math
import operator
import os
import re
import sqlite3
import threading
import time
from array import array
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Protocol
from urllib.parse import urlsplit

from app_paths import app_data_dir
from lesson_metadata import (
    _frontmatter_bounds,
    _source_checked_date,
    _source_review_interval_days,
    _source_review_schedule,
)
from trusted_sources import TrustedSourceMonitor

logger = logging.getLogger("colidev.knowledge")

_CHUNK_CHARS = 1200
_MAX_FILE_BYTES = 512 * 1024
_MAX_DOCUMENTS = 2000
_MAX_TOTAL_BYTES = 64 * 1024 * 1024
_MAX_RESULTS_PER_DOCUMENT = 2
# Keyword scoring normalises length against fixed reference lengths, close to
# the course averages in October 2026, rather than the live corpus average:
# lengthening lessons in one subject must not flip close rankings elsewhere.
# Длина нормируется по фиксированным опорным значениям (близким к средним курса
# на октябрь 2026), а не по средней живого корпуса: рост уроков одного предмета
# не должен переворачивать близкие места в другом.
_REFERENCE_CHUNK_TOKENS = 64
_REFERENCE_DOCUMENT_TOKENS = 1024
# A passage ranks by its own keyword match plus its whole lesson's match, each
# scaled to the best score for the question, so a lesson that is about the
# question beats one paragraph that merely repeats its words.
# Фрагмент оценивается по своему совпадению плюс совпадению всего урока (оба
# делятся на лучший результат по вопросу): урок по теме вопроса обгоняет абзац,
# где просто повторяются слова запроса.
_DOCUMENT_SCORE_WEIGHT = 1.0
_MIN_SEMANTIC_SIMILARITY = 0.25
# Reciprocal-rank fusion of the keyword and vector rankings. With equal weights
# a chunk sharing one incidental word outranked the best meaning match; weight 3
# for vectors was tuned on rag_eval_questions.json and confirmed on the holdout
# set (project-plan/research/rag-semantic-search-and-tutor-model-2026-10-26.md).
# Слияние рангов (RRF) по словам и по векторам. При равных весах фрагмент с одним
# случайным общим словом обгонял лучший ответ по смыслу; вес 3 для векторов подобран
# на rag_eval_questions.json и подтверждён на контрольном наборе.
_RRF_K = 60
_LEXICAL_WEIGHT = 1.0
_SEMANTIC_WEIGHT = 3.0
_FUSION_CANDIDATES: int | None = None
_EMBEDDING_BATCH_SIZE = 16
# A question may embed one small batch inline (for example, a short edited
# note). Larger gaps, such as the first full-corpus pass, which takes minutes
# on an M1, are filled by a background thread while keyword search answers.
# Внутри вопроса досчитывается не больше одного пакета (например, короткий
# изменённый урок). Большие пропуски, как первый проход по всему корпусу (минуты
# на M1), заполняет фоновый поток, пока отвечает поиск по словам.
_INLINE_EMBEDDING_CHUNKS = _EMBEDDING_BATCH_SIZE
_EMBEDDING_RETRY_SECONDS = 60
# Some embedding families expect an instruction on the query side only.
# Некоторым моделям эмбеддингов нужна инструкция только перед вопросом.
_QUERY_INSTRUCTIONS = {
    "qwen3-embedding": (
        "Instruct: Given a student's study question, retrieve course passages that answer it\nQuery: "
    ),
}
_IGNORED_DIRS = {
    ".git", ".obsidian", "__pycache__", "build", "dist", "node_modules", "vendor",
}
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)
_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how",
    "in", "into", "is", "it", "of", "on", "or", "that", "the", "this", "to",
    "was", "what", "when", "where", "which", "with", "you",
    "в", "во", "для", "до", "же", "за", "и", "из", "или", "как", "к", "на",
    "над", "не", "но", "о", "об", "от", "по", "под", "при", "про", "с", "со",
    "то", "у", "что", "это",
}


class EmbeddingProvider(Protocol):
    model: str

    def embed(self, texts: list[str]) -> list[list[float]]: ...


def default_database_path() -> Path:
    """Return a per-user writable database path on macOS, Windows, or Linux."""
    return app_data_dir() / "knowledge.sqlite3"


def _utc_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _tokens(text: str) -> list[str]:
    return [token for token in _TOKEN_RE.findall(text.casefold()) if len(token) >= 2 and token not in _STOP_WORDS]


def _expanded_tokens(tokens: Iterable[str]) -> list[str]:
    result: list[str] = []
    for token in tokens:
        result.append(token)
        # A lightweight prefix match helps RU/EN inflected forms without
        # pretending this keyword index is a full morphological search engine.
        if len(token) >= 6:
            result.append(token[:5])
    return result


def _split_markdown(
    text: str,
    fallback_heading: str,
    *,
    allow_frontmatter: bool = True,
) -> list[tuple[int, int, str, str]]:
    """Split Markdown into bounded heading-aware chunks with source line spans."""
    lines = text.splitlines()
    frontmatter = _frontmatter_bounds(lines) if allow_frontmatter else None
    indexed_lines = [
        (line_number, line)
        for line_number, line in enumerate(lines, start=1)
        if frontmatter is None or not frontmatter[0] <= line_number - 1 <= frontmatter[1]
    ]
    chunks: list[tuple[int, int, str, str]] = []
    heading = fallback_heading
    buffer: list[str] = []
    buffer_chars = 0
    start_line = 1
    end_line = 1

    def flush() -> None:
        nonlocal buffer, buffer_chars
        value = "\n".join(buffer).strip()
        if value:
            chunks.append((start_line, end_line, heading, value))
        buffer = []
        buffer_chars = 0

    for line_number, line in indexed_lines:
        heading_match = _HEADING_RE.match(line)
        if heading_match:
            flush()
            heading = heading_match.group(1).strip()[:200] or fallback_heading
            start_line = line_number
            end_line = line_number
            continue

        # Keep a single unusually long line within the same safety bound.
        pieces = [line[index:index + _CHUNK_CHARS] for index in range(0, len(line), _CHUNK_CHARS)] or [""]
        for piece in pieces:
            added = len(piece) + (1 if buffer else 0)
            if buffer and buffer_chars + added > _CHUNK_CHARS:
                flush()
                start_line = line_number
            if not buffer:
                start_line = line_number
            buffer.append(piece)
            buffer_chars += len(piece) + (1 if len(buffer) > 1 else 0)
            end_line = line_number

    flush()
    body_text = "\n".join(line for _, line in indexed_lines).strip()
    if not chunks and body_text:
        first_line = indexed_lines[0][0]
        last_line = indexed_lines[-1][0]
        chunks.append((first_line, last_line, fallback_heading, body_text[:_CHUNK_CHARS]))
    return chunks


@dataclass
class _DocumentTerms:
    frequencies: Counter[str]
    length: int
    title: set[str]
    path: set[str]


def _inverse_frequency(count: int, frequency: int) -> float:
    return math.log(1 + (count - frequency + 0.5) / (frequency + 0.5))


def _saturated_frequency(term_frequency: int, length: int, reference_length: int) -> float:
    """BM25 term weight (k1 = 1.2, b = 0.75) against a fixed reference length."""
    return term_frequency * 2.2 / (term_frequency + 1.2 * (0.25 + 0.75 * length / reference_length))


def _document_scores(documents: dict[str, _DocumentTerms], query_terms: set[str]) -> dict[str, float]:
    """Score whole lessons, so passages from a lesson about the question rank higher."""
    document_frequency: Counter[str] = Counter()
    for document in documents.values():
        document_frequency.update(set(document.frequencies) | document.title | document.path)
    count = len(documents)
    scores: dict[str, float] = {}
    for path, document in documents.items():
        score = 0.0
        for term in query_terms:
            term_frequency = document.frequencies[term]
            in_title = term in document.title
            if not term_frequency and not in_title:
                continue
            inverse_frequency = _inverse_frequency(count, document_frequency[term])
            if term_frequency:
                score += inverse_frequency * _saturated_frequency(
                    term_frequency, document.length, _REFERENCE_DOCUMENT_TOKENS
                )
            if in_title:
                score += inverse_frequency * 1.5
            if term in document.path:
                score += inverse_frequency * 0.5
        if score > 0:
            scores[path] = score
    return scores


class OllamaEmbeddingProvider:
    """Generate vectors with a local Ollama server without using HTTP proxies."""

    def __init__(self, base_url: str, model: str, timeout_seconds: float = 12) -> None:
        normalized_url = base_url.strip().rstrip("/")
        try:
            parsed = urlsplit(normalized_url)
            hostname = parsed.hostname
            parsed.port
        except ValueError as error:
            raise ValueError("Ollama embedding URL is invalid") from error
        if (
            parsed.scheme.lower() not in {"http", "https"}
            or not hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Ollama embeddings require a loopback HTTP(S) URL")
        normalized_host = hostname.lower().removesuffix(".")
        try:
            address = ipaddress.ip_address(normalized_host)
            is_loopback = address.is_loopback or (
                isinstance(address, ipaddress.IPv6Address)
                and address.ipv4_mapped is not None
                and address.ipv4_mapped.is_loopback
            )
        except ValueError:
            is_loopback = normalized_host == "localhost"
        if not is_loopback:
            raise ValueError("Ollama embeddings are restricted to loopback endpoints")
        if not model.strip() or len(model) > 200:
            raise ValueError("Ollama embedding model name is required")
        self.base_url = normalized_url
        self.model_name = model.strip()
        self.model = f"ollama:{self.base_url}:{self.model_name}"
        self.timeout_seconds = max(1, min(float(timeout_seconds), 120))
        family = self.model_name.rsplit("/", 1)[-1].split(":", 1)[0].casefold()
        self.query_instruction = _QUERY_INSTRUCTIONS.get(family, "")

    def embed_query(self, text: str) -> list[list[float]]:
        """Embed a search question, adding the model family's query instruction."""
        return self.embed([f"{self.query_instruction}{text}"])

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts or len(texts) > _EMBEDDING_BATCH_SIZE or any(not text.strip() for text in texts):
            raise ValueError("Ollama embedding input must contain 1 to 16 non-empty texts")
        import httpx

        with httpx.Client(
            trust_env=False,
            follow_redirects=False,
            timeout=httpx.Timeout(self.timeout_seconds, connect=2),
        ) as client:
            response = client.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model_name, "input": texts},
            )
            response.raise_for_status()
            payload = response.json()
        embeddings = payload.get("embeddings") if isinstance(payload, dict) else None
        if not isinstance(embeddings, list):
            raise ValueError("Ollama embedding response is missing embeddings")
        return embeddings


class KnowledgeIndex:
    """Incremental SQLite index for approved local learning materials."""

    _SOURCE_ROOTS = (
        (Path("02_Areas"), frozenset({".md"})),
        (Path("03_Resources") / "Cheatsheets", frozenset({".md", ".txt"})),
    )

    def __init__(
        self,
        project_root: Path,
        database_path: Path | None = None,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> None:
        self.project_root = project_root.resolve()
        self.database_path = (database_path or default_database_path()).expanduser()
        self.embedding_provider = embedding_provider
        self._lock = threading.RLock()
        self._embedding_retry_after = 0.0
        self._warmup_lock = threading.Lock()
        self._warmup_thread: threading.Thread | None = None
        # Decoded unit vectors keyed by chunk and tagged with the document digest,
        # so each question does not re-parse megabytes of JSON from SQLite.
        # Разобранные единичные векторы по фрагментам с хешем документа, чтобы
        # каждый вопрос не разбирал заново мегабайты JSON из SQLite.
        self._vector_cache_model: str | None = None
        self._vector_cache: dict[tuple[str, int], tuple[str, array]] = {}

    def set_embedding_provider(self, provider: EmbeddingProvider | None) -> None:
        """Switch the local embedding route and clear any previous failure backoff."""
        with self._lock:
            self.embedding_provider = provider
            self._embedding_retry_after = 0.0

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    @staticmethod
    def _ensure_schema(connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                path TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                digest TEXT NOT NULL,
                modified_ns INTEGER NOT NULL,
                size_bytes INTEGER NOT NULL,
                modified_at TEXT NOT NULL,
                source_checked_at TEXT,
                source_review_interval_days INTEGER,
                source_references_json TEXT NOT NULL DEFAULT '[]'
            )
            """
        )
        document_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(documents)").fetchall()
        }
        if "source_checked_at" not in document_columns:
            connection.execute("ALTER TABLE documents ADD COLUMN source_checked_at TEXT")
        if "source_review_interval_days" not in document_columns:
            connection.execute("ALTER TABLE documents ADD COLUMN source_review_interval_days INTEGER")
        if "source_references_json" not in document_columns:
            connection.execute(
                "ALTER TABLE documents ADD COLUMN source_references_json TEXT NOT NULL DEFAULT '[]'"
            )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                path TEXT NOT NULL REFERENCES documents(path) ON DELETE CASCADE,
                chunk_index INTEGER NOT NULL,
                heading TEXT NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                text TEXT NOT NULL,
                PRIMARY KEY (path, chunk_index)
            )
            """
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS index_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS chunk_embeddings (
                path TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                model TEXT NOT NULL,
                vector_json TEXT NOT NULL,
                PRIMARY KEY (path, chunk_index, model),
                FOREIGN KEY (path, chunk_index)
                    REFERENCES chunks(path, chunk_index) ON DELETE CASCADE
            )
            """
        )

    def _scan_documents(self) -> tuple[list[Path], bool]:
        documents: list[Path] = []
        complete = True
        total_bytes = 0

        for relative_root, extensions in self._SOURCE_ROOTS:
            source_root = self.project_root / relative_root
            if source_root.is_symlink():
                logger.warning("Skipping symlink knowledge root", extra={"path": str(relative_root)})
                continue
            if not source_root.is_dir():
                continue

            errors: list[OSError] = []

            def record_walk_error(error: OSError) -> None:
                errors.append(error)

            for current_root, directory_names, file_names in os.walk(
                source_root, topdown=True, followlinks=False, onerror=record_walk_error
            ):
                current_path = Path(current_root)
                directory_names[:] = [
                    name for name in directory_names
                    if not name.startswith(".")
                    and name not in _IGNORED_DIRS
                    and not (current_path / name).is_symlink()
                ]
                for name in sorted(file_names, key=str.casefold):
                    if name.startswith("."):
                        continue
                    path = current_path / name
                    if path.is_symlink() or path.suffix.casefold() not in extensions:
                        continue
                    try:
                        path.resolve(strict=True).relative_to(self.project_root)
                    except (OSError, ValueError):
                        continue
                    documents.append(path)
                    if len(documents) >= _MAX_DOCUMENTS:
                        complete = False
                        break
                if len(documents) >= _MAX_DOCUMENTS:
                    break

            if errors:
                complete = False
                logger.warning("Knowledge scan was incomplete", extra={"root": str(relative_root)})

            if len(documents) >= _MAX_DOCUMENTS:
                break

        documents.sort(key=lambda path: path.relative_to(self.project_root).as_posix().casefold())
        bounded: list[Path] = []
        for path in documents:
            try:
                size = path.stat().st_size
            except OSError:
                complete = False
                continue
            if total_bytes + size > _MAX_TOTAL_BYTES:
                complete = False
                break
            bounded.append(path)
            total_bytes += size
        return bounded, complete

    @staticmethod
    def _document_title(relative_path: str, content: str) -> str:
        for line in content.splitlines():
            match = _HEADING_RE.match(line)
            if match:
                return match.group(1).strip()[:200] or Path(relative_path).stem
        return Path(relative_path).stem.replace("_", " ").replace("-", " ")

    def refresh_sources(self) -> dict[str, str | int | None]:
        """Refresh the approved local course corpus without running embeddings."""
        self.refresh_and_search("", limit=0, refresh_only=True)
        return self.status()

    def refresh_and_search(
        self,
        query: str,
        limit: int = 4,
        *,
        refresh_only: bool = False,
    ) -> list[dict[str, Any]]:
        """Refresh changed files and return relevant excerpts for an offline RAG prompt."""
        normalized_query = query.strip()[:500]
        if not refresh_only and (not normalized_query or limit <= 0):
            return []

        with self._lock:
            connection = self._connect()
            try:
                self._ensure_schema(connection)
                paths, scan_complete = self._scan_documents()
                seen_paths: set[str] = set()
                accepted_bytes = 0

                with connection:
                    for path in paths:
                        relative_path = path.relative_to(self.project_root).as_posix()
                        seen_paths.add(relative_path)
                        try:
                            before = path.stat()
                            if before.st_size > _MAX_FILE_BYTES:
                                connection.execute("DELETE FROM documents WHERE path = ?", (relative_path,))
                                continue
                            if accepted_bytes + before.st_size > _MAX_TOTAL_BYTES:
                                scan_complete = False
                                break

                            raw = path.read_bytes()
                            after = path.stat()
                        except OSError:
                            scan_complete = False
                            continue

                        if (
                            before.st_size != after.st_size
                            or before.st_mtime_ns != after.st_mtime_ns
                            or len(raw) != after.st_size
                        ):
                            # A file was being edited as it was read. Keep its cached
                            # version and retry on the next request.
                            scan_complete = False
                            continue

                        accepted_bytes += len(raw)
                        digest = hashlib.sha256(raw).hexdigest()
                        modified_at = _utc_timestamp(after.st_mtime)
                        content = raw.decode("utf-8", errors="replace")
                        is_markdown = path.suffix.casefold() == ".md"
                        source_checked_at = _source_checked_date(content) if is_markdown else None
                        source_review_interval_days = (
                            _source_review_interval_days(content) if is_markdown else None
                        )
                        source_references_json = json.dumps(
                            TrustedSourceMonitor.approved_markdown_links(content) if is_markdown else [],
                            ensure_ascii=False,
                            separators=(",", ":"),
                        )
                        current = connection.execute(
                            "SELECT digest, title FROM documents WHERE path = ?",
                            (relative_path,),
                        ).fetchone()
                        if current and current["digest"] == digest:
                            connection.execute(
                                """UPDATE documents
                                   SET modified_ns = ?, size_bytes = ?, modified_at = ?, source_checked_at = ?,
                                       source_review_interval_days = ?, source_references_json = ?
                                   WHERE path = ?""",
                                (
                                    after.st_mtime_ns, after.st_size, modified_at, source_checked_at,
                                    source_review_interval_days, source_references_json, relative_path,
                                ),
                            )
                            continue

                        title = self._document_title(relative_path, content)
                        connection.execute("DELETE FROM documents WHERE path = ?", (relative_path,))
                        connection.execute(
                            """
                            INSERT INTO documents(
                                path, title, digest, modified_ns, size_bytes, modified_at,
                                source_checked_at, source_review_interval_days, source_references_json
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                relative_path, title, digest, after.st_mtime_ns,
                                after.st_size, modified_at, source_checked_at, source_review_interval_days,
                                source_references_json,
                            ),
                        )
                        chunks = _split_markdown(content, title, allow_frontmatter=is_markdown)
                        connection.executemany(
                            """
                            INSERT INTO chunks(path, chunk_index, heading, start_line, end_line, text)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            [
                                (relative_path, index, heading, start, end, chunk)
                                for index, (start, end, heading, chunk) in enumerate(chunks)
                            ],
                        )

                    if scan_complete:
                        connection.executemany(
                            "DELETE FROM documents WHERE path = ?",
                            [
                                (row["path"],)
                                for row in connection.execute("SELECT path FROM documents").fetchall()
                                if row["path"] not in seen_paths
                            ],
                        )
                    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
                    connection.execute(
                        """
                        INSERT INTO index_meta(key, value) VALUES ('last_checked_at', ?)
                        ON CONFLICT(key) DO UPDATE SET value = excluded.value
                        """,
                        (checked_at,),
                    )

                if refresh_only:
                    return []

                semantic = self._prepare_embeddings(connection, normalized_query)
                query_vector, document_vectors = semantic if semantic else (None, None)
                return self._search(
                    connection,
                    normalized_query,
                    max(1, min(limit, 8)),
                    query_vector=query_vector,
                    document_vectors=document_vectors,
                )
            finally:
                connection.close()

    @staticmethod
    def _normalise_vectors(vectors: object, expected_count: int) -> list[list[float]]:
        if not isinstance(vectors, list) or len(vectors) != expected_count:
            raise ValueError("Embedding provider returned an unexpected vector count")
        normalized: list[list[float]] = []
        expected_dimension: int | None = None
        for vector in vectors:
            if not isinstance(vector, (list, tuple)) or not 1 <= len(vector) <= 4096:
                raise ValueError("Embedding provider returned an invalid vector")
            if expected_dimension is None:
                expected_dimension = len(vector)
            if len(vector) != expected_dimension:
                raise ValueError("Embedding provider returned inconsistent dimensions")
            values = [float(value) for value in vector]
            if not all(math.isfinite(value) for value in values):
                raise ValueError("Embedding provider returned a non-finite value")
            magnitude = math.sqrt(sum(value * value for value in values))
            if magnitude <= 0:
                raise ValueError("Embedding provider returned a zero vector")
            normalized.append([value / magnitude for value in values])
        return normalized

    @staticmethod
    def _decode_vector(value: str) -> list[float] | None:
        try:
            parsed = json.loads(value)
            if not isinstance(parsed, list):
                return None
            return KnowledgeIndex._normalise_vectors([parsed], 1)[0]
        except (TypeError, ValueError, OverflowError, json.JSONDecodeError):
            return None

    @staticmethod
    def _active_model(provider: EmbeddingProvider | None) -> str | None:
        model = getattr(provider, "model", None)
        return model if provider is not None and isinstance(model, str) and model.strip() else None

    def _embedding_failed(self, error: Exception) -> None:
        # Ollama is optional. A missing model, timeout, or malformed response
        # must never make curated offline keyword retrieval unavailable.
        # Ollama необязательна: нет модели, таймаут или кривой ответ не должны
        # отключать офлайн-поиск по словам.
        self._embedding_retry_after = time.monotonic() + _EMBEDDING_RETRY_SECONDS
        logger.info(
            "Local embeddings unavailable; using lexical search",
            extra={"error_type": type(error).__name__},
        )

    def _load_document_vectors(
        self, connection: sqlite3.Connection, model: str
    ) -> tuple[list[sqlite3.Row], dict[tuple[str, int], array]]:
        """Return chunks that still lack a vector and the cached vectors of the rest."""
        chunk_rows = connection.execute(
            """
            SELECT c.path, c.chunk_index, d.digest, d.title, c.heading, c.text
            FROM chunks AS c JOIN documents AS d ON d.path = c.path
            ORDER BY c.path, c.chunk_index
            """
        ).fetchall()
        if self._vector_cache_model != model:
            self._vector_cache_model = model
            self._vector_cache = {}
        cache = self._vector_cache
        live = {(row["path"], row["chunk_index"]): row["digest"] for row in chunk_rows}
        for key in [key for key, (digest, _) in cache.items() if live.get(key) != digest]:
            del cache[key]

        stale_paths = sorted({
            row["path"] for row in chunk_rows if (row["path"], row["chunk_index"]) not in cache
        })
        for path in stale_paths:
            for row in connection.execute(
                "SELECT chunk_index, vector_json FROM chunk_embeddings WHERE model = ? AND path = ?",
                (model, path),
            ).fetchall():
                key = (path, row["chunk_index"])
                if key not in live or key in cache:
                    continue
                vector = self._decode_vector(row["vector_json"])
                if vector is None:
                    connection.execute(
                        "DELETE FROM chunk_embeddings WHERE path = ? AND chunk_index = ? AND model = ?",
                        (path, row["chunk_index"], model),
                    )
                    continue
                cache[key] = (live[key], array("d", vector))

        if len({len(vector) for _, vector in cache.values()}) > 1:
            # A model tag should have one vector shape. Discard mixed cache data
            # and rebuild it instead of silently mixing incompatible vectors.
            connection.execute("DELETE FROM chunk_embeddings WHERE model = ?", (model,))
            cache.clear()
        connection.commit()

        missing = [row for row in chunk_rows if (row["path"], row["chunk_index"]) not in cache]
        return missing, {key: vector for key, (_, vector) in cache.items()}

    @classmethod
    def _embed_rows(cls, provider: EmbeddingProvider, rows: list[sqlite3.Row]) -> list[list[float]]:
        texts = [f"{row['title']}\n{row['heading']}\n{row['path']}\n{row['text']}" for row in rows]
        return cls._normalise_vectors(provider.embed(texts), len(rows))

    def _store_vectors(
        self,
        connection: sqlite3.Connection,
        model: str,
        rows: list[sqlite3.Row],
        vectors: list[list[float]],
    ) -> None:
        dimensions = {len(vector) for _, vector in self._vector_cache.values()}
        if len({len(vector) for vector in vectors}) != 1 or (
            dimensions and len(vectors[0]) not in dimensions
        ):
            raise ValueError("Embedding dimension changed for the configured model")
        for row, vector in zip(rows, vectors, strict=True):
            # The digest guard drops a vector computed for a lesson that was
            # edited while the background pass was waiting for Ollama.
            # Проверка хеша отбрасывает вектор урока, изменённого, пока фоновый
            # проход ждал Ollama.
            stored = connection.execute(
                """
                INSERT OR REPLACE INTO chunk_embeddings(path, chunk_index, model, vector_json)
                SELECT ?, ?, ?, ?
                WHERE EXISTS (SELECT 1 FROM documents WHERE path = ? AND digest = ?)
                """,
                (
                    row["path"], row["chunk_index"], model,
                    json.dumps(vector, separators=(",", ":")), row["path"], row["digest"],
                ),
            ).rowcount
            if stored and self._vector_cache_model == model:
                self._vector_cache[(row["path"], row["chunk_index"])] = (row["digest"], array("d", vector))
        connection.commit()

    def warm_embeddings(self) -> bool:
        """Embed every indexed chunk that lacks a vector; True when the cache is complete.

        Ollama is called outside the index lock, so questions keep getting
        keyword answers while the first full pass runs.
        """
        provider = self.embedding_provider
        model = self._active_model(provider)
        if model is None or time.monotonic() < self._embedding_retry_after:
            return False
        max_rounds: int | None = None
        try:
            while True:
                with self._lock:
                    if self.embedding_provider is not provider:
                        return False
                    connection = self._connect()
                    try:
                        self._ensure_schema(connection)
                        missing, _ = self._load_document_vectors(connection, model)
                    finally:
                        connection.close()
                if not missing:
                    return True
                if max_rounds is None:
                    # Allow for lessons edited mid-pass, but never loop forever.
                    # Учитываем уроки, изменённые во время прохода, но без бесконечного цикла.
                    max_rounds = 2 * math.ceil(len(missing) / _EMBEDDING_BATCH_SIZE) + 2
                max_rounds -= 1
                if max_rounds < 0:
                    return False
                batch = missing[:_EMBEDDING_BATCH_SIZE]
                vectors = self._embed_rows(provider, batch)
                with self._lock:
                    if self.embedding_provider is not provider:
                        return False
                    connection = self._connect()
                    try:
                        self._store_vectors(connection, model, batch, vectors)
                    finally:
                        connection.close()
        except Exception as error:
            self._embedding_failed(error)
            return False

    def start_embedding_warmup(self) -> bool:
        """Fill missing vectors in a daemon thread; False if not needed or already running."""
        if self._active_model(self.embedding_provider) is None or (
            time.monotonic() < self._embedding_retry_after
        ):
            return False
        with self._warmup_lock:
            if self._warmup_thread is not None and self._warmup_thread.is_alive():
                return False
            self._warmup_thread = threading.Thread(
                target=self.warm_embeddings, name="colidev-embedding-warmup", daemon=True
            )
            self._warmup_thread.start()
        return True

    def _prepare_embeddings(
        self, connection: sqlite3.Connection, query: str
    ) -> tuple[list[float], dict[tuple[str, int], array]] | None:
        """Best-effort local embeddings; lexical retrieval remains the fallback."""
        provider = self.embedding_provider
        model = self._active_model(provider)
        if model is None or time.monotonic() < self._embedding_retry_after:
            return None
        try:
            missing, vectors = self._load_document_vectors(connection, model)
            if not missing and not vectors:
                return None
            if len(missing) > _INLINE_EMBEDDING_CHUNKS:
                self.start_embedding_warmup()
                return None
            if missing:
                self._store_vectors(connection, model, missing, self._embed_rows(provider, missing))
                missing, vectors = self._load_document_vectors(connection, model)
                if missing:
                    return None

            embed_query = getattr(provider, "embed_query", None)
            query_vectors = embed_query(query) if callable(embed_query) else provider.embed([query])
            query_vector = self._normalise_vectors(query_vectors, 1)[0]
            if len(query_vector) != len(next(iter(vectors.values()))):
                raise ValueError("Query embedding dimension does not match indexed vectors")
            return query_vector, vectors
        except Exception as error:
            self._embedding_failed(error)
            return None

    def _search(
        self,
        connection: sqlite3.Connection,
        query: str,
        limit: int,
        query_vector: list[float] | None = None,
        document_vectors: dict[tuple[str, int], array] | None = None,
    ) -> list[dict[str, Any]]:
        rows = connection.execute(
            """
            SELECT c.path, d.title, d.modified_at, d.source_checked_at,
                   d.source_review_interval_days, d.source_references_json, c.heading, c.start_line,
                   c.end_line, c.text, c.chunk_index
            FROM chunks AS c
            JOIN documents AS d ON d.path = c.path
            """
        ).fetchall()
        if not rows:
            return []

        query_terms = set(_expanded_tokens(_tokens(query)))
        if not query_terms and query_vector is None:
            return []

        parsed: list[tuple[sqlite3.Row, list[str], Counter[str], set[str], set[str], set[str]]] = []
        document_frequency: Counter[str] = Counter()
        documents: dict[str, _DocumentTerms] = {}
        for row in rows:
            body_tokens = _expanded_tokens(_tokens(row["text"]))
            heading_tokens = set(_expanded_tokens(_tokens(row["heading"])))
            title_tokens = set(_expanded_tokens(_tokens(row["title"])))
            path_tokens = set(_expanded_tokens(_tokens(row["path"].replace("/", " "))))
            frequencies = Counter(body_tokens + list(heading_tokens) + list(title_tokens) + list(path_tokens))
            terms = set(frequencies)
            document_frequency.update(terms)
            parsed.append((row, body_tokens, frequencies, heading_tokens, title_tokens, path_tokens))
            document = documents.setdefault(
                row["path"], _DocumentTerms(Counter(), 0, title_tokens, path_tokens)
            )
            document.frequencies.update(body_tokens)
            document.frequencies.update(heading_tokens)
            document.length += max(1, len(body_tokens))

        count = len(parsed)
        lexical_ranked: list[tuple[float, sqlite3.Row]] = []
        for row, body_tokens, frequencies, heading_tokens, title_tokens, path_tokens in parsed:
            length = max(1, len(body_tokens))
            score = 0.0
            for term in query_terms:
                term_frequency = frequencies[term]
                if not term_frequency:
                    continue
                inverse_frequency = _inverse_frequency(count, document_frequency[term])
                score += inverse_frequency * _saturated_frequency(
                    term_frequency, length, _REFERENCE_CHUNK_TOKENS
                )
                if term in heading_tokens:
                    score += inverse_frequency * 1.25
                if term in title_tokens:
                    score += inverse_frequency * 1.5
                if term in path_tokens:
                    score += inverse_frequency * 0.5
            if score > 0:
                lexical_ranked.append((score, row))

        document_scores = _document_scores(documents, query_terms)
        if lexical_ranked and document_scores:
            best_chunk = max(score for score, _ in lexical_ranked)
            best_document = max(document_scores.values())
            lexical_ranked = [
                (
                    score / best_chunk
                    + _DOCUMENT_SCORE_WEIGHT * document_scores.get(row["path"], 0.0) / best_document,
                    row,
                )
                for score, row in lexical_ranked
            ]

        lexical_ranked.sort(
            key=lambda pair: (-pair[0], pair[1]["path"].casefold(), pair[1]["chunk_index"])
        )
        ranked: list[tuple[float, sqlite3.Row]] = lexical_ranked
        keys = [(item[0]["path"], item[0]["chunk_index"]) for item in parsed]
        if (
            query_vector
            and document_vectors
            and all(key in document_vectors for key in keys)
            and {len(document_vectors[key]) for key in keys} == {len(query_vector)}
        ):
            scored_semantic = [
                (sum(map(operator.mul, query_vector, document_vectors[key])), item)
                for key, item in zip(keys, parsed, strict=True)
            ]
            semantic_ranked = [
                item for similarity, item in sorted(
                    scored_semantic,
                    key=lambda pair: (
                        -pair[0], pair[1][0]["path"].casefold(), pair[1][0]["chunk_index"]
                    ),
                )
                if similarity >= _MIN_SEMANTIC_SIMILARITY
            ]
            fused: dict[tuple[str, int], float] = {}
            row_by_key: dict[tuple[str, int], sqlite3.Row] = {}
            lexical_scores: dict[tuple[str, int], float] = {}
            for rank, (score, row) in enumerate(lexical_ranked[:_FUSION_CANDIDATES], start=1):
                key = (row["path"], row["chunk_index"])
                fused[key] = fused.get(key, 0.0) + _LEXICAL_WEIGHT / (_RRF_K + rank)
                row_by_key[key] = row
                lexical_scores[key] = score
            for rank, item in enumerate(semantic_ranked[:_FUSION_CANDIDATES], start=1):
                row = item[0]
                key = (row["path"], row["chunk_index"])
                fused[key] = fused.get(key, 0.0) + _SEMANTIC_WEIGHT / (_RRF_K + rank)
                row_by_key[key] = row
            ranked = [
                (fused[key], row_by_key[key])
                for key in sorted(
                    fused,
                    key=lambda key: (
                        -fused[key],
                        -lexical_scores.get(key, 0.0),
                        key[0].casefold(),
                        key[1],
                    ),
                )
            ]
        retrieved_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
        results: list[dict[str, Any]] = []
        per_document: Counter[str] = Counter()
        for _, row in ranked:
            if per_document[row["path"]] >= _MAX_RESULTS_PER_DOCUMENT:
                continue
            per_document[row["path"]] += 1
            excerpt = row["text"].strip()[:_CHUNK_CHARS]
            if row["heading"] and row["heading"].casefold() not in excerpt.casefold():
                excerpt = f"{row['heading']}\n{excerpt}"[:_CHUNK_CHARS + 200]
            result = {
                "title": row["title"],
                "excerpt": excerpt,
                "retrieved_at": retrieved_at,
                "modified_at": row["modified_at"],
                "path": row["path"],
                "location": f"{row['start_line']}-{row['end_line']}",
                "source_type": "course",
            }
            try:
                stored_references = json.loads(row["source_references_json"])
            except (TypeError, json.JSONDecodeError):
                stored_references = []
            if isinstance(stored_references, list):
                official_references = [
                    {"title": item["title"], "url": item["url"]}
                    for item in stored_references[:20]
                    if isinstance(item, dict)
                    and isinstance(item.get("title"), str)
                    and isinstance(item.get("url"), str)
                ]
                if official_references:
                    result["official_references"] = official_references
            if row["source_checked_at"]:
                result["source_checked_at"] = row["source_checked_at"]
            if row["source_review_interval_days"] is not None:
                result["source_review_interval_days"] = str(row["source_review_interval_days"])
                due_on, review_status = _source_review_schedule(
                    row["source_checked_at"], row["source_review_interval_days"]
                )
                if due_on and review_status:
                    result["source_review_due_on"] = due_on
                    result["source_review_status"] = review_status
            results.append(result)
            if len(results) >= limit:
                break
        return results

    def embedding_status(self) -> dict[str, int | bool]:
        """Report how much of the course has vectors for the active embedding model."""
        model = self._active_model(self.embedding_provider)
        result: dict[str, int | bool] = {
            "chunk_count": 0, "embedded_chunk_count": 0, "semantic_ready": False,
        }
        if not self.database_path.exists():
            return result
        with self._lock:
            connection = self._connect()
            try:
                self._ensure_schema(connection)
                connection.commit()
                total = int(connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])
                embedded = 0
                if model is not None:
                    embedded = int(connection.execute(
                        """
                        SELECT COUNT(*) FROM chunk_embeddings AS e
                        JOIN chunks AS c ON c.path = e.path AND c.chunk_index = e.chunk_index
                        WHERE e.model = ?
                        """,
                        (model,),
                    ).fetchone()[0])
            except sqlite3.Error:
                return result
            finally:
                connection.close()
        result.update({
            "chunk_count": total,
            "embedded_chunk_count": embedded,
            "semantic_ready": model is not None and total > 0 and embedded == total,
        })
        return result

    def status(self) -> dict[str, str | int | None]:
        """Return persisted index metadata without triggering a rescan."""
        if not self.database_path.exists():
            return {
                "document_count": 0,
                "last_checked_at": None,
                "review_due_document_count": 0,
                "review_scheduled_document_count": 0,
                "review_schedule_missing_document_count": 0,
            }
        with self._lock:
            connection = self._connect()
            try:
                # Additive migrations also run when Settings requests health,
                # so older per-user indexes can report review metadata safely.
                self._ensure_schema(connection)
                connection.commit()
                count = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
                checked = connection.execute(
                    "SELECT value FROM index_meta WHERE key = 'last_checked_at'"
                ).fetchone()
                review_due_count = 0
                review_scheduled_count = 0
                review_schedule_missing_count = 0
                rows = connection.execute(
                    "SELECT source_checked_at, source_review_interval_days FROM documents"
                ).fetchall()
                for row in rows:
                    _, review_status = _source_review_schedule(
                        row["source_checked_at"], row["source_review_interval_days"]
                    )
                    if review_status == "due":
                        review_due_count += 1
                    elif review_status == "scheduled":
                        review_scheduled_count += 1
                    else:
                        review_schedule_missing_count += 1
                return {
                    "document_count": int(count),
                    "last_checked_at": checked[0] if checked else None,
                    "review_due_document_count": review_due_count,
                    "review_scheduled_document_count": review_scheduled_count,
                    "review_schedule_missing_document_count": review_schedule_missing_count,
                }
            except sqlite3.Error:
                return {
                    "document_count": 0,
                    "last_checked_at": None,
                    "review_due_document_count": 0,
                    "review_scheduled_document_count": 0,
                    "review_schedule_missing_document_count": 0,
                }
            finally:
                connection.close()
