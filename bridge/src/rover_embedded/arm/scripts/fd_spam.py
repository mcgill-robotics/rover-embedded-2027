"""
Spam CAN FD frames out of the CANable so there's something to look at
on the logic analyzer. Nothing else. No MQTT, no ESC protocol.

    uv run python src/rover_embedded/arm/scripts/fd_spam.py --port /dev/serial/by-id/usb-...

Ctrl+C to stop.

Heads up: if nothing else is on the bus to ACK the frame, the CANable will
just keep retrying the same frame and eventually go error-passive. You should
STILL see bits on the wire though (the frame + error flags), so "nothing at
all" means a wiring/probe/termination/open-bus problem, not a missing ACK.
"""

import argparse
import itertools
import time

import can

from rover_embedded.arm.esc_can.protocol import ARB_BITRATE, DATA_BITRATE


def main() -> None:
    parser = argparse.ArgumentParser(description="Send CAN FD frames forever.")
    parser.add_argument("--port", default="/dev/ttyACM0",
                        help="CANable serial device (use the /dev/serial/by-id/ path)")
    parser.add_argument("--id", type=lambda s: int(s, 0), default=0x123,
                        help="arbitration ID, e.g. 0x123 (default 0x123)")
    parser.add_argument("--period", type=float, default=0.1,
                        help="seconds between frames (default 0.1)")
    parser.add_argument("--len", type=int, default=16,
                        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64],
                        help="payload bytes (>8 so it's obviously FD, default 16)")
    parser.add_argument("--no-brs", action="store_true",
                        help="don't switch to the data bitrate (whole frame at nominal rate)")
    args = parser.parse_args()

    bus = can.Bus(
        interface="slcan",
        channel=f"{args.port}@115200",
        bitrate=ARB_BITRATE,          # 500 kbps
        data_bitrate=DATA_BITRATE,    # 2 Mbps
        fd=True,
    )
    print(f"Opened {args.port}: {ARB_BITRATE} / {DATA_BITRATE} bps, "
          f"ID 0x{args.id:03X}, {args.len} bytes, BRS {'off' if args.no_brs else 'on'}")

    try:
        for n in itertools.count():
            # 0x55 = 01010101: easy to spot as a square wave on the analyzer.
            # First byte is a counter so you can tell frames apart.
            data = bytes([n & 0xFF]) + b"\x55" * (args.len - 1) if args.len else b""
            msg = can.Message(
                arbitration_id=args.id,
                is_extended_id=args.id > 0x7FF,
                is_fd=True,
                bitrate_switch=not args.no_brs,
                data=data,
            )
            try:
                bus.send(msg)
                print(f"\rsent {n + 1}", end="", flush=True)
            except can.CanError as exc:
                print(f"\nsend failed: {exc}")
            time.sleep(args.period)
    except KeyboardInterrupt:
        print("\nstopping")
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
