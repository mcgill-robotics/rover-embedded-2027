# Library Consumer CMake

This is an example STM32 CMake project that uses two libraries.

See [`CMakeLists.txt`](./CMakeLists.txt) to see how the libraries are imported and [`Core`](./Core/) for the firmware's code.

The code for the libraries can be found at [library_command_parser](../library_command_parser/) and [library_uart_handler](../library_uart_handler/). 

The firmware allows blinking the LED on a nucleo G474 board by sending commands over the Virtual COM Port interface on it's USB port.

The expected command format is `l` or `s` followed bit little endian integer. with `l`, the number will be interpreted as a boolean to turn it on or off and with `s` as the blinking rate in milliseconds.

The [`command_script`](./command_script.py) script is provided for convenience to send commands.

**Example commands**:

`l0`: Disable LED blinking
`l1`: Enable LED blinking
`s1000`: Set blinking rate to 1 second
`s500`: Set blinking rate to 500 milliseconds