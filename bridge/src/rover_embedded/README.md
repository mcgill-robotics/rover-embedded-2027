# rover_embedded

## Overview

This is the main module consumed by the software division. It exposes all the APIs to control the boards on the rover.

## Boards

`arm/brushed_board_firmware.py`: Control of the brushed motor controller on the arm's end effector (and science's auger)

`power/power_board_cli.py`: CLI to control the secondary kill switch and the headlights from the Jetson.

`science/science_board_logger.py`: Data collection and logging of sensor data to csv files.
