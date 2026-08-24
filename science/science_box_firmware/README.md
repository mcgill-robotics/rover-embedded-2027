# Science Box Firmware

Firmware for the Science Board

## About

This firmware implements reading from PH, Moisture and CO2 sensors and reporting the measurements over USB to assist in automated onboard experiments on the rover. Data from a Time of Flight sensor is also available but has not been used for the experiments.

A companion script to this firmware is available in the `rover-embedded` package in the `bridge` directory of this repository [here](../../bridge/src/rover_embedded/science/science_board_logger.py). The companion script helps collect all the data and save it to csv files.