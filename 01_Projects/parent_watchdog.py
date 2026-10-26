"""Stop the bundled backend when the ColiDev app that launched it is gone.

The app terminates the backend on a normal quit, but a crash, a force quit, or a quit after the
window was closed can skip that path and leave an orphaned server holding a port and memory.
macOS reparents an orphan to launchd, so a changed parent PID is a reliable signal to shut down.

Останавливает встроенный backend, если запустившее его приложение ColiDev завершилось.
"""

from __future__ import annotations

import logging
import os
import signal
import threading
from typing import Callable

PARENT_PID_ENV = "COLIDEV_PARENT_PID"

logger = logging.getLogger(__name__)


def _request_graceful_shutdown() -> None:
    # SIGTERM lets uvicorn run its normal shutdown instead of exiting mid-request.
    os.kill(os.getpid(), signal.SIGTERM)


def expected_parent_pid(environ: dict[str, str] | None = None) -> int | None:
    """Return the app PID passed by the launcher, or None when the backend runs standalone."""
    raw = (environ if environ is not None else os.environ).get(PARENT_PID_ENV, "").strip()
    if not raw.isdigit():
        return None
    pid = int(raw)
    return pid if pid > 1 else None


def start_parent_watchdog(
    parent_pid: int | None,
    *,
    interval_seconds: float = 2.0,
    getppid: Callable[[], int] = os.getppid,
    on_orphaned: Callable[[], None] = _request_graceful_shutdown,
) -> threading.Thread | None:
    """Watch the parent in a daemon thread; call ``on_orphaned`` once when it disappears.

    The watchdog arms only when the backend is still a direct child of ``parent_pid`` at start,
    so a backend launched some other way (tests, a terminal, an intermediate launcher) is never
    stopped by mistake. / Сторож включается, только если backend — прямой потомок приложения.
    """
    if parent_pid is None or interval_seconds <= 0:
        return None
    if getppid() != parent_pid:
        logger.warning("Parent watchdog not armed: parent PID does not match %s", PARENT_PID_ENV)
        return None

    stopped = threading.Event()

    def watch() -> None:
        while not stopped.wait(interval_seconds):
            if getppid() != parent_pid:
                logger.warning("ColiDev app exited; stopping the orphaned backend")
                stopped.set()
                on_orphaned()
                return

    thread = threading.Thread(target=watch, name="colidev-parent-watchdog", daemon=True)
    thread.stop_event = stopped  # type: ignore[attr-defined]
    thread.start()
    return thread


def start_parent_watchdog_from_env() -> threading.Thread | None:
    return start_parent_watchdog(expected_parent_pid())
