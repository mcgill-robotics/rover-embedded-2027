"""
This is a helper file for the other tests.
It makes a broker for the other tests to use.

if you don't have mosquitto do this: sudo apt install mosquitto

Thank you for using TonyCode today. We hope your experience was delightful.
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

# The below is a pytest fixture. It's a flag for pytest to let it know that 
# it's a helper function for other tests.
# E.G. it's added to a function argument and then the results are passed in.
# Or whatever. I'm not 100% sure myself.
@pytest.fixture(scope="session")
def mqtt_broker(tmp_path_factory):
    """Start a private Mosquitto for the whole test session, yield (host, port)."""
    # Red fish stay, blue fish go, give me your environment variable for mosquitto.
    exe = os.environ.get("MOSQUITTO") or shutil.which("mosquitto")
    if exe is None:
        pytest.skip("mosquitto not installed (sudo apt install mosquitto)")

    port = _free_port()
    # Create a temporary config file.
    conf = tmp_path_factory.mktemp("mosquitto") / "test.conf"
    # Listen to local traffic and don't require a login.
    conf.write_text(f"listener {port} 127.0.0.1\nallow_anonymous true\n")

    # Create the process using the config file.
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
