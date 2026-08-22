cmake_minimum_required(VERSION 3.22)

include_guard(GLOBAL)

find_package(Git QUIET)

# Submodule update from https://cliutils.gitlab.io/modern-cmake/submodule/
function(update_submodules)
    if(GIT_FOUND)
    # Update submodules as needed
        option(GIT_SUBMODULE "Check submodules during build" ON)
        if(GIT_SUBMODULE)
            message(STATUS "Updating submodules")
            execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive
                            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                            RESULT_VARIABLE GIT_SUBMOD_RESULT)
            if(NOT GIT_SUBMOD_RESULT EQUAL "0")
                message(FATAL_ERROR "git submodule update --init --recursive failed with code ${GIT_SUBMOD_RESULT}, please checkout submodules")
            endif()
            execute_process(COMMAND ${GIT_EXECUTABLE} submodule sync
                            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                            RESULT_VARIABLE GIT_SUBMOD_SYNC_RESULT)
            if(NOT GIT_SUBMOD_SYNC_RESULT EQUAL "0")
                message(FATAL_ERROR "git submodule sync failed with ${GIT_SUBMOD_SYNC_RESULT}, please checkout submodules")
            endif()
        endif()
    endif()
endfunction()

# Modified from https://cliutils.gitlab.io/modern-cmake/submodule/
function(get_commit_hash COMMIT_HASH_VARIABLE)
    if(GIT_FOUND)
        execute_process(COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
            WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
            OUTPUT_VARIABLE PACKAGE_GIT_VERSION
            ERROR_QUIET
            OUTPUT_STRIP_TRAILING_WHITESPACE)
        set(${COMMIT_HASH_VARIABLE} ${PACKAGE_GIT_VERSION} PARENT_SCOPE)
    endif()
endfunction()
