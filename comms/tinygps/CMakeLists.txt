cmake_minimum_required(VERSION 3.22)
enable_language(C CXX ASM)

# Import Library Versioning Tool
include(../../other/cmake/version-checker.cmake)

# Set library information
set_lib_info("tinygps" 0.1.0)

add_library(tinygps STATIC
    ${CMAKE_CURRENT_LIST_DIR}/tinygps.cpp
    ${CMAKE_CURRENT_LIST_DIR}/tinyubx.c
)

target_include_directories(tinygps PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(${LIBRARY_NAME}
    stm32cubemx
    # Add user defined libraries
)
