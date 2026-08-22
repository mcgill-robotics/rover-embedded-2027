# This file defines functions to be used in CmakeLists.txt
# to help version internal libraries within the rover-embedded monorepo
# It also handles third party libraries by ignoring versioning and
# prevents duplicate source directory inclusions even for transitive 
# dependencies

include_guard(GLOBAL)

# Get python for check_version_match
find_package(Python3 REQUIRED Interpreter)
if (NOT Python3_Interpreter_FOUND)
	message(SEND_ERROR "Could not check version: No python was found")
endif()

# Function to perform more complex version checks than the built-in cmake ones
# Python is used because it is much easier to deal with the versioning
# parsing than in pure cmake language
function(check_version_match)
	# Args: ACTUAL, EXPECTED, POLICY
	if (${ARGC} EQUAL 3)
		set(EXEC_CODE 2)
		set(SCRIPT_OUTPUT)
		set(SCRIPT_ERROR_OUTPUT)
		execute_process(
			COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/version-checker.py ${ARGV}
			WORKING_DIRECTORY ${CMAKE_CURRENT_FUNCTION_LIST_DIR}
			RESULT_VARIABLE EXEC_CODE 
			OUTPUT_VARIABLE SCRIPT_OUTPUT 
			ERROR_VARIABLE SCRIPT_ERROR_OUTPUT
		)
		if (EXEC_CODE EQUAL 0)
			if (SCRIPT_OUTPUT)
				message(STATUS ${SCRIPT_OUTPUT})
			endif()
			message(STATUS "Found compatible library version ${ARGV0}")
		else()
			message(SEND_ERROR 
				" Version Mismatch with policy ${ARGV2}:\n"
			 	" Found: ${ARGV0}\n" 
				" Expected: ${ARGV1}" 
			)
			# message(SEND_ERROR ${SCRIPT_ERROR_OUTPUT})
		endif()
	else()
		message(SEND_ERROR "Missing Arguments: Need Actual Version, Expected Version and Policy")
	endif()
endfunction()

# Macro to set library metadata in CmakeLists.txt
macro(set_lib_info)
	if (${ARGC} GREATER_EQUAL 2)
		set(LIBRARY_NAME ${ARGV0} PARENT_SCOPE)
		set(ACTUAL_LIB_VERSION ${ARGV1} PARENT_SCOPE)
		# Also set in current scope so lib can read it itself
		set(LIBRARY_NAME ${ARGV0})
		set(ACTUAL_LIB_VERSION ${ARGV1})
	endif()
endmacro()

# Helper function to get global lists as we need the list to persist
# for all CMakeLists.txt
macro(list_global LIST_MODE GLOBAL_LIST)
	get_property(TEMP_LIST_VAR GLOBAL PROPERTY ${GLOBAL_LIST})
	list(${LIST_MODE} TEMP_LIST_VAR ${ARGN})
	set_property(GLOBAL PROPERTY ${GLOBAL_LIST} ${TEMP_LIST_VAR})
	unset(TEMP_LIST_VAR)
endmacro()

function(use_lib)
	if (${ARGC} GREATER_EQUAL 3)
		# Arg 1 is subdirectory
		# Arg 2 is version
		# Arg 3 is version match policy
		# Arg 4 is optional build directory
		set(REQUIRED_LIB_VERSION ${ARGV1})
		
		# Setup global library list if first invocation
		get_property(LIBRARY_PATH_LIST_EXISTS
			GLOBAL
			PROPERTY LIBRARY_PATH_LIST
			DEFINED
		)
		if (NOT LIBRARY_PATH_LIST_EXISTS)
			define_property(GLOBAL PROPERTY LIBRARY_PATH_LIST)
			define_property(GLOBAL PROPERTY LIBRARY_NAME_LIST)
			define_property(GLOBAL PROPERTY LIBRARY_VERSION_LIST)
		endif()

		# Save current values for variables
		if (DEFINED ACTUAL_LIB_VERSION)
			set(SAVED_VERSION ${ACTUAL_LIB_VERSION})
		endif()

		if (DEFINED LIBRARY_NAME)
			set(SAVED_NAME ${LIBRARY_NAME})
			unset(LIBRARY_NAME)
		endif()

		# Create variables for checking duplicates
		set(LIBRARY_ABSOLUTE_PATH)
		set(LIBRARY_LIST_INDEX)

		# Get library absolute path to detect duplicates
		file(REAL_PATH ${ARGV0} LIBRARY_ABSOLUTE_PATH EXPAND_TILDE)
		# Check for duplicate entry
		list_global(FIND LIBRARY_PATH_LIST ${LIBRARY_ABSOLUTE_PATH} LIBRARY_LIST_INDEX)

		if (NOT LIBRARY_LIST_INDEX EQUAL -1)
			# Send message for already imported libs
			set(LIBRARY_NAME)
			set(ACTUAL_LIB_VERSION)
			list_global(GET LIBRARY_NAME_LIST ${LIBRARY_LIST_INDEX} LIBRARY_NAME)
			list_global(GET LIBRARY_VERSION_LIST ${LIBRARY_LIST_INDEX} ACTUAL_LIB_VERSION)
			message(STATUS "Library ${LIBRARY_NAME} already found with version ${ACTUAL_LIB_VERSION}")
		else()
			# Setup Lib
			add_subdirectory(${ARGV0} ${ARGV3})

			# If third party or info missing set name to unknown
			if (NOT DEFINED LIBRARY_NAME)
				set(LIBRARY_NAME "Unknown Library")
			endif()

			message(STATUS "Using library ${LIBRARY_NAME} ${REQUIRED_LIB_VERSION} at path ${ARGV0}")

			# Update global library list for duplicate checks
			list_global(APPEND LIBRARY_PATH_LIST ${LIBRARY_ABSOLUTE_PATH})
			list_global(APPEND LIBRARY_NAME_LIST ${LIBRARY_NAME})
			# Make sure lists always have a value even if no info is known
			if (NOT DEFINED ACTUAL_LIB_VERSION)
				set(LIBRARY_NAME "Unknown Library")
				list_global(APPEND LIBRARY_VERSION_LIST "0.0.0-unknown")
			else()
				list_global(APPEND LIBRARY_VERSION_LIST ${ACTUAL_LIB_VERSION})
			endif()
			
		endif()
	
		# Verify versions
		if (ARGV2 STREQUAL "ANY")
			message(STATUS "No required version for ${LIBRARY_NAME}")
		else()
			if(DEFINED ACTUAL_LIB_VERSION)
				check_version_match(${ACTUAL_LIB_VERSION} ${REQUIRED_LIB_VERSION} ${ARGV2})
			else()
				message(SEND_ERROR "Library does not define a version")
			endif()
		endif()

		# Clean up info after use to avoid conflicts
		unset(ACTUAL_LIB_VERSION)
		unset(LIBRARY_NAME)

		# Restore old values
		if (DEFINED SAVED_VERSION)
			set(ACTUAL_LIB_VERSION ${SAVED_VERSION})
		endif()

		if (DEFINED SAVED_NAME)
			set(LIBRARY_NAME ${SAVED_NAME})
		endif()
	else()
		message(SEND_ERROR "No version was given")
	endif()
endfunction()