cmake_minimum_required(VERSION 3.22)
enable_language(C CXX ASM)

project("tinygps" VERSION 0.1.1)

# Import Library Versioning Tool
include(../../other/cmake/version-checker.cmake)

# Set library information
set_lib_info("tinygps" 0.1.0)

add_library(${LIBRARY_NAME} STATIC
    src/tinygps.cpp
    src/tinyubx.c
)

target_include_directories(${LIBRARY_NAME} PUBLIC
    include/
)

target_link_libraries(${LIBRARY_NAME}
    stm32cubemx
    # Add user defined libraries
)
