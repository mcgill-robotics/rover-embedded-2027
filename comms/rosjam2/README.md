# ROSjam2

A standard USB communication library for McGill Robotics' Rover

## About

Currently this library is a thin wrapper over [tinyusb](https://github.com/hathach/tinyusb) to facilitate implementing communication over a USB-CDC interface. It also abstracts some of the configuration for setting custom info in the descriptors to make devices unique.

Future versions may implement a standardized communication protocol on top of
the USB-CDC interface to provide information about the firmware, diagnostics and more.