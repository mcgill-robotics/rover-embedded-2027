# GPS

Firmware for the Uart Board. 

## About

This firmware handles reading one or two GPS connected to the Uart Board and sends position data over USB.
It also handles forwarding commands to the pantilt board and multiplexing data at the same time to a UART from the USB interface.

All data sent over USB is framed using COBS and prefixed with an ascii character to allow multiplexing arbitrary binary data for the GPS, Pantilt and the remaining free UART connection.

A control API for this firmware is available in the `rover-embedded` package in the `bridge` directory of this repository [here](../../bridge/src/rover_embedded/comms/pantilt_firmware.py).