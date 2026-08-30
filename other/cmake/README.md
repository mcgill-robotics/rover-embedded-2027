# CMake Scripts

Miscellaneous CMake scripts to make builds simpler.

# Scripts

`git-helper.cmake`: Helper functions to fetch commit information, fetch submodules, etc.

`version-checker.cmake`: Local path based dependency resolver for use in this monorepo. Allows versioning libraries added using CMake's `add_subdirectory` with semantic versioning while verifying compatibility and preventing duplicate inclusions even with transitive dependencies. The comparison method is implemented using the `version-checker.py` script.