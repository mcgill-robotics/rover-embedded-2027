# Brushed Board Firmware

Firmware for the Arm Brushed Board.

## About

The firmware supports communication over USB to control the three joints on the
end effector (Wrist Pitch, Wrist Roll, Gripper).

The Wrist Pitch joint can be configured to be controlled by rotation direction  or PID controlled at runtime. All other joints can be controlled by their rotation direction.

An early control API for this firmware is available in the `rover-embedded` package in the `bridge` directory of this repository [here](../../bridge/src/rover_embedded/arm/brushed_board_firmware.py).

A web based ui with a control server supporting all the current features is available in the [controls](./controls/) subdirectory.