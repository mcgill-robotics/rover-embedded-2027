# Blinky CMake

This is an example STM32 CMake project for blinking
an LED on a Nucleo-G474RE. The code is found in the [`Core`](./Core) folder.

The firmware defines a `Toggle_LED` function in [`led.c`](./Core/Src/led.c) to demonstrate how to add extra source files in the [`CMakeLists.txt`](./CMakeLists.txt)