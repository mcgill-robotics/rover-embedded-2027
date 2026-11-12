cmake_minimum_required(VERSION 3.22)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project("rosjam2" VERSION 0.1.1)
enable_language(C CXX ASM)

#Import Git Helper
include(../../other/cmake/git-helper.cmake)

# Import Library Versioning Tool
include(../../other/cmake/version-checker.cmake)

# Set library information
set_lib_info("rosjam2" 0.2.0)

# Create static library
add_library(${LIBRARY_NAME} STATIC)

# Add dependencies
update_submodules()
use_lib(${CMAKE_CURRENT_SOURCE_DIR}/libs/tinyusb/src "Unknown Version" ANY "${CMAKE_CURRENT_BINARY_DIR}/tinyusb_build")
use_lib(${CMAKE_CURRENT_SOURCE_DIR}/../cobs-c 0.2.0 APPROX "${CMAKE_CURRENT_BINARY_DIR}/cobs_build")

# Add header file locations

target_include_directories(${LIBRARY_NAME} PUBLIC 
  include/
)

# Add source files
target_sources(${LIBRARY_NAME} PUBLIC 
  # Source files go here
  src/rosjam.c
  src/usb_descriptors.c
  src/bp_buffer.c

  libs/tinyusb/src/portable/st/stm32_fsdev/dcd_stm32_fsdev.c
  libs/tinyusb/src/portable/st/stm32_fsdev/fsdev_common.c
  libs/tinyusb/src/portable/st/typec/typec_stm32.c
  
)

tinyusb_target_add(${LIBRARY_NAME})

target_link_libraries(${LIBRARY_NAME}
    stm32cubemx
    # Add user defined libraries
    cobs-c
)