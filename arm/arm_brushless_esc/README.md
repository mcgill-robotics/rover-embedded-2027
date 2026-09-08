# Arm Brushless ESCs

This folder contains the firmware for the Arm Brushless ESCs and scripts to test
them.

## Navigation

`arm_elbow_esc`, `arm_shoulder_esc`, `arm_waist_esc`: CMake based STM32CubeMX projects
for the firmware. If you need to make changes to firwmare it will be in these folders.

`scripts`: useful python scripts to test the firmware and launch control ui. Will require to install the 
`rover-embedded` package in [`bridge`](../../bridge/).

`arm_elbow_esc.stwb6`, `arm_shoulder_esc.stwb6`, `arm_waist_esc.stwb6`: ST Motor Workshop
projects to auto-generate the STM32CubeMX projects with code for generating the three phases
needed for our BLDC motors based on profiling.