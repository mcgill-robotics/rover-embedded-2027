# Library Command Parser

This is an example library that does not rely on the STM32 HAL. 

The code for the library is in [`src`](./src/). In that folder there is a [`CMakeLists.txt`](./src/CMakeLists.txt) that defines helps define the library.

The [`CMakeLists.txt`](./CMakeLists.txt) in this folder is used to build an executable that can be used to test the library (see the [test](./test/) folder). 

This library parses commands of the form `<letter><number>`
where the letter is either `l` or `s` and the number is a little-endian 32-bit integer from a buffer of bytes.