"""
Shared pytest fixtures.

mqtt_broker spins up a throwaway Mosquitto on a free port for the integration
tests, so it never collides with the system service (if you have one running).
If Mosquitto isn't installed, those tests get skipped instead of failing.

Install it with: sudo apt install mosquitto
"""

import os
import shutil
import socket
import subprocess
import time

import pytest


def _free_port() -> int:
    "Ask the OS for an unused port."
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def mqtt_broker(tmp_path_factory):
    """Start a private Mosquitto for the whole test session, yield (host, port)."""
    exe = os.environ.get("MOSQUITTO") or shutil.which("mosquitto")
    if exe is None:
        pytest.skip("mosquitto not installed (sudo apt install mosquitto)")

    port = _free_port()
    conf = tmp_path_factory.mktemp("mosquitto") / "test.conf"
    conf.write_text(f"listener {port} 127.0.0.1\nallow_anonymous true\n")

    proc = subprocess.Popen([exe, "-c", str(conf)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait until it's actually accepting connections.
    deadline = time.monotonic() + 3
    while True:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.1).close()
            break
        except OSError:
            if proc.poll() is not None or time.monotonic() > deadline:
                proc.kill()
                pytest.fail("mosquitto did not start")
            time.sleep(0.05)

    yield ("127.0.0.1", port)

    proc.terminate()
    proc.wait(timeout=2)
