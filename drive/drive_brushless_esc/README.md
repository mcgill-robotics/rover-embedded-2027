# Drive Brushless ESCs

This folder contains the firmware for the Drive Brushless ESCs and scripts to test
it.

## Navigation

`drive_esc_firmware`, `arm_shoulder_esc`, `arm_waist_esc`: CMake based STM32CubeMX project
for the firmware. If you need to make changes to firwmare it will be in this folder.

`scripts`: useful python scripts to test the firmware. Will likely require to install the 
`rover-embedded` package in [`bridge`](../../bridge/).

`drive_esc_firmware.stwb6`: ST Motor Workshop
project to auto-generate the STM32CubeMX project with code for generating the three phases
needed for our BLDC motors based on profiling.