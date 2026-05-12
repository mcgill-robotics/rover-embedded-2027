# rover-embedded-2027

Welcome to our repo for the 2026-2027 school year.

This repo contains the code we use for custom boards and other embedded targets within rover's electrical division.

## Table of Contents

- [rover-embedded-2027](#rover-embedded-2027)
	- [Table of Contents](#table-of-contents)
	- [Navigation](#navigation)
	- [Tasks](#tasks)
	- [Guidelines](#guidelines)
	- [Tooling and environment](#tooling-and-environment)


## Navigation

The repo is mostly organized by subsystems in the rover

`arm`: Projects relating to arm control

`comms`: Projecta relating to communication interfaces on the rover(USB, RS-485, CAN, GPS, etc.)

`drive`: Projects for drive system controls(Steering, Drive, etc.)

`power`: Projects relating to the power system (Power board monitoring etc.)

`science`: Projects relating to electrical support tasks for the science division (science board)

`bridge`: Python packages to communicate between our firmware and our software division's ROS and MQTT services.

`examples`: Example projects used for tutorials and for quick testing on custom board bring-up.

`other`: Other miscellaneous projects and scripts that don't fit any of the other categories.

## Tasks 

Tasks in our division can be found on our Kanban board [here](https://github.com/orgs/mcgill-robotics/projects/70)

## Guidelines

To keep the repo nice and organized so its easy to work in, please try to follow as closely as possible the guidelines in the [rover electrical handbook]().

## Tooling and environment

Most of our projects are built using STM32CubeIDEs integrated build system and thus requires it for builds. Some select projects may use CMake as the build system and are compatible with any IDE supporting CMake or the command line for builds. Within the team, VSCode and STM32CubeIDE are used for these projects. A few legacy systems using Arduino cores rely on PlatformIO for builds. These are typically built by us using VSCode.

For our Python scripts, common dependencies are [pyserial](https://github.com/pyserial/pyserial) and [python-can](https://python-can.readthedocs.io/en/stable/). More details on exact dependencies can be found in project READMEs. Most scripts support both Linux and Windows as they are deployed on Linux for the rover and a majoritu of members use Windows on rheir development machines. MacOS should also be supported but is less tested as it is more uncommon in the team.
