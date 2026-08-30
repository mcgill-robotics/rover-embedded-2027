# Bridge

## Overview

Packaged python scripts and libraries. These often are used to communicate between 
our computers and various boards over USB or CAN. The code in here can be both 
used for internal use or used by the software division's controls.

# Installation

See [`INSTALL.md`](./INSTALL.md) 

## Navigation

`src`: Source code for the libraries and scripts packaged in the rover-embedded
package. See the [Sub-Projects](#sub-projects) section for how the code is oragnized.

`pyproject.toml`: Package definition with dependencies and versioning and 
exporting scripts as standalone commands.

`hatch_build.py`: Metadata hook for adding commit as build metadata to versions
when building the rover-embedded package.

## Sub-Projects

`rover_embedded`: The main package containing the APIs for controlling the rover's boards. 
This package is organized by the subsystems each API controls.
See that [`README.md`](./src/rover_embedded/README.md) in the folder for more information on the supported boards.

`cobs_py`: An implementation of [COBS](https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing)
 in Python for use in communication protocols.

