cmake_minimum_required(VERSION 3.22)

# Setup compiler settings
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

enable_language(C CXX ASM)

# Import Library Versioning Tool
include(../../other/cmake/version-checker.cmake)

# Set library information
set_lib_info("cobs-c" 0.2.0)

# Create static library
add_library(${LIBRARY_NAME} STATIC)

# Add dependencies


# Add header file locations
target_include_directories(${LIBRARY_NAME} PUBLIC 
  include/
)

# Add source files
target_sources(${LIBRARY_NAME} PUBLIC 
  # Source files go here
  src/cobs.c
)

target_link_libraries(${LIBRARY_NAME}
    # Add user defined libraries
)

# Prevent Running GoogleTest when compiling for embedded targets
if(CMAKE_CROSSCOMPILING STREQUAL FALSE)
project()
set(GTEST_EXECUTABLE_NAME cobs-test)
# Add GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/063de7e9578f82b369302001269680b4b1553359.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
include(GoogleTest)

add_executable(${GTEST_EXECUTABLE_NAME})

# Add sources to executable
target_sources(${GTEST_EXECUTABLE_NAME} PRIVATE
    # Add user sources here
    # "test/test.c"
    test/cobs_test.cc
)

# Add include paths
target_include_directories(${GTEST_EXECUTABLE_NAME} PRIVATE
    # Add user defined include paths
)
# Add linked libraries
target_link_libraries(${GTEST_EXECUTABLE_NAME}
    # Add user defined libraries
    ${LIBRARY_NAME}
    GTest::gtest_main
)

gtest_discover_tests(${GTEST_EXECUTABLE_NAME})
enable_testing()

endif()