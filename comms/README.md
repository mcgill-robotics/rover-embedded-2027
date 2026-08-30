# Comms subsystem

## Overview

This directory contains embedded code relating to communication between the Jetson, Pi and base station.

## Projects

`cobs-c`: A c implementation of [COBS](https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing) for use in communication protocols.

`gps`: Firmware for the Uart Board to collect GPS data and send pantilt commands.

`pantilt`: Firmware for the pantilt board to control the pantilt camera servos.

`rosjam2`: USB communication library

`tinygps`: GPS data format parsing library. A fork of [TinyGPSPlus](https://github.com/mikalhart/TinyGPSPlus) for STM32 HAL and with added features.