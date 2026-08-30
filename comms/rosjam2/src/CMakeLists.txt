cmake_minimum_required(VERSION 3.22)
enable_language(C CXX ASM)
#Import Git Helper
include(../../../other/cmake/git-helper.cmake)

# Import Library Versioning Tool
include(../../../other/cmake/version-checker.cmake)

# Set library information
set_lib_info("rosjam2" 0.1.0)

# Create static library
add_library(${LIBRARY_NAME} STATIC)

# Add dependencies
update_submodules()
use_lib(${CMAKE_CURRENT_SOURCE_DIR}/../libs/tinyusb/src "Unknown Version" ANY "${CMAKE_CURRENT_BINARY_DIR}/tinyusb_build")

# Add header file locations
target_include_directories(${LIBRARY_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Add source files
target_sources(${LIBRARY_NAME} PUBLIC 
  # Source files go here
  ${CMAKE_CURRENT_SOURCE_DIR}/rosjam.c
  ${CMAKE_CURRENT_SOURCE_DIR}/usb_descriptors.c

  ${CMAKE_CURRENT_SOURCE_DIR}/../libs/tinyusb/src/portable/st/stm32_fsdev/dcd_stm32_fsdev.c
  ${CMAKE_CURRENT_SOURCE_DIR}/../libs/tinyusb/src/portable/st/stm32_fsdev/fsdev_common.c
  ${CMAKE_CURRENT_SOURCE_DIR}/../libs/tinyusb/src/portable/st/typec/typec_stm32.c
)

tinyusb_target_add(${LIBRARY_NAME})

target_link_libraries(${LIBRARY_NAME}
    stm32cubemx
    # Add user defined libraries
)
