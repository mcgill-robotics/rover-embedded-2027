cmake_minimum_required(VERSION 3.22)
enable_language(C CXX ASM)

# Import Library Versioning Tool
include(../../../other/cmake/version-checker.cmake)

# Set library information
set_lib_info("uart-handler" 0.1.0)

# Create static library
add_library(${LIBRARY_NAME} STATIC)

# Add dependencies

# Add header file locations
target_include_directories(${LIBRARY_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Add source files
target_sources(${LIBRARY_NAME} PUBLIC 
  # Source files go here
  ${CMAKE_CURRENT_SOURCE_DIR}/uart_handler.c
)

target_link_libraries(${LIBRARY_NAME}
    stm32cubemx
    # Add user defined libraries
)
