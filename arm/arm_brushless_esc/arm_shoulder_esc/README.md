# Arm Shoulder ESC firmware

Firmware for the Arm Shoulder ESCs controlling a BLDC motor

## Notes

To open the .ioc for this project the ST MCSDK v.6.4.2 is necessary.

If importing this as a CMake project in STM32CubeMX, use `STM32G431CBUx` when asked
for the MCU. VSCode should auto-detect it but if it doesnt use the same thing.

Header files (`.h`) are in [`Inc`](./Inc/) and source files (`.c`) are in [`Src`](./Src/)