import os
import subprocess
import sys
import textwrap
import threading
import time
from pathlib import Path

from parent_watchdog import PARENT_PID_ENV, expected_parent_pid, start_parent_watchdog

PROJECT_DIR = Path(__file__).resolve().parent


def test_expected_parent_pid_reads_only_valid_pids():
    assert expected_parent_pid({PARENT_PID_ENV: "4242"}) == 4242
    assert expected_parent_pid({PARENT_PID_ENV: " 4242 "}) == 4242
    assert expected_parent_pid({}) is None
    assert expected_parent_pid({PARENT_PID_ENV: ""}) is None
    assert expected_parent_pid({PARENT_PID_ENV: "abc"}) is None
    assert expected_parent_pid({PARENT_PID_ENV: "-5"}) is None
    # PID 1 is launchd: a backend parented to it is already orphaned, never a valid app PID.
    assert expected_parent_pid({PARENT_PID_ENV: "1"}) is None


def test_watchdog_stops_backend_once_parent_is_gone():
    parents = iter([4242, 4242, 4242, 1])
    orphaned = threading.Event()
    calls = []

    def fake_getppid():
        return next(parents, 1)

    def on_orphaned():
        calls.append("stop")
        orphaned.set()

    thread = start_parent_watchdog(
        4242, interval_seconds=0.01, getppid=fake_getppid, on_orphaned=on_orphaned
    )
    assert thread is not None and thread.daemon
    assert orphaned.wait(2)
    thread.join(2)
    assert not thread.is_alive()
    assert calls == ["stop"]


def test_watchdog_keeps_running_while_parent_is_alive():
    calls = []
    thread = start_parent_watchdog(
        4242, interval_seconds=0.01, getppid=lambda: 4242, on_orphaned=lambda: calls.append("stop")
    )
    assert thread is not None
    thread.join(0.1)
    assert thread.is_alive() and calls == []
    thread.stop_event.set()
    thread.join(2)
    assert not thread.is_alive()


def test_watchdog_is_not_armed_without_a_matching_parent():
    calls = []
    assert start_parent_watchdog(None, getppid=lambda: 4242, on_orphaned=lambda: calls.append("x")) is None
    # Launched by something other than the app (terminal, tests): never stop it by mistake.
    assert start_parent_watchdog(4242, getppid=lambda: 777, on_orphaned=lambda: calls.append("x")) is None
    assert start_parent_watchdog(4242, interval_seconds=0, getppid=lambda: 4242) is None
    assert calls == []


def _pid_is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def test_real_child_exits_after_its_parent_dies_abruptly():
    # A launcher process starts a backend-like child with the watchdog, prints its PID, and dies
    # without any cleanup (like a crash or force quit). The child must then stop on its own.
    # Процесс-«приложение» умирает без очистки; дочерний процесс должен завершиться сам.
    child_code = textwrap.dedent(
        """
        import sys, time
        from parent_watchdog import start_parent_watchdog_from_env
        print("armed" if start_parent_watchdog_from_env() is not None else "not-armed", flush=True)
        sys.stdout.close()
        while True:
            time.sleep(0.05)
        """
    )
    # The launcher waits until the child reports an armed watchdog, so the test cannot pass merely
    # because the child failed to start. / Ждём, пока сторож включится, иначе тест прошёл бы зря.
    launcher_code = textwrap.dedent(
        f"""
        import os, subprocess, sys
        env = dict(os.environ, {PARENT_PID_ENV}=str(os.getpid()))
        child = subprocess.Popen(
            [sys.executable, "-c", {child_code!r}],
            env=env, cwd={str(PROJECT_DIR)!r}, stdout=subprocess.PIPE, text=True,
        )
        state = child.stdout.readline().strip()
        print(child.pid, state, flush=True)
        os._exit(0)
        """
    )
    env = dict(os.environ, PYTHONPATH=str(PROJECT_DIR))
    started = time.monotonic()
    launcher = subprocess.run(
        [sys.executable, "-c", launcher_code], env=env, capture_output=True, text=True, timeout=20
    )
    assert launcher.returncode == 0, launcher.stderr
    child_pid_text, state = launcher.stdout.split()
    child_pid = int(child_pid_text)
    assert state == "armed"

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline and _pid_is_running(child_pid):
        time.sleep(0.1)
    still_running = _pid_is_running(child_pid)
    if still_running:
        os.kill(child_pid, 9)
    assert not still_running, "orphaned child kept running after its parent died"
    # It stopped through the watchdog's 2-second check, not by crashing at start.
    assert time.monotonic() - started >= 1.5
