# To kill System2, write in terminal:   python power_board_cli.py PORT kill
# To unkill System2, write in terminal: python power_board_cli.py PORT unkill
# To toggle the headlights on, type in the terminal:  python power_board_cli.py PORT lights_on 
# To toggle the headlights off, type in the terminal: python power_board_cli.py PORT lights_off
# Make sure you modify your port properly 

import serial
import time
import sys
import pathlib

# PORT = "COM6"  # Change this to the correct port
BAUDRATE = 9600
def main():
    # Argument check
    if len(sys.argv) != 3:
        executable_path = pathlib.Path(sys.argv[0])
        if executable_path.suffix == ".py":
            command = f"python {executable_path.name}"
        else:
            command = executable_path.name
        print(f"Usage: {command} PORT [kill|unkill|lights_on|lights_off]")
        sys.exit(1)

    cmd = sys.argv[2].lower()
    PORT = sys.argv[1]
    if cmd not in ["kill", "unkill", "lights_on", "lights_off"]:
        print("Invalid argument. Use 'kill', 'unkill', 'lights_on' or 'lights_off'.")
        sys.exit(1)

    # Map command to byte
    cmd_map = {
        "kill": b'Kill_H',
        "unkill": b'Kill_L',
        "lights_on": b'Light_H',
        "lights_off": b'Light_L',
    }

    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            time.sleep(2)  # Wait for Teensy to initialize
            ser.write(cmd_map[cmd])
            print(f"Sent command '{cmd}' to Teensy on {PORT}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()