# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.6

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/CMake/3.6.3/bin/cmake

# The command to remove a file.
RM = /cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/CMake/3.6.3/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /scratch/rg18646/DD4HEP/lcgeo

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /scratch/rg18646/DD4HEP/lcgeo/build

# Utility rule file for ContinuousBuild.

# Include the progress variables for this target.
include CMakeFiles/ContinuousBuild.dir/progress.make

CMakeFiles/ContinuousBuild:
	/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/CMake/3.6.3/bin/ctest -D ContinuousBuild

ContinuousBuild: CMakeFiles/ContinuousBuild
ContinuousBuild: CMakeFiles/ContinuousBuild.dir/build.make

.PHONY : ContinuousBuild

# Rule to build all files generated by this target.
CMakeFiles/ContinuousBuild.dir/build: ContinuousBuild

.PHONY : CMakeFiles/ContinuousBuild.dir/build

CMakeFiles/ContinuousBuild.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ContinuousBuild.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ContinuousBuild.dir/clean

CMakeFiles/ContinuousBuild.dir/depend:
	cd /scratch/rg18646/DD4HEP/lcgeo/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /scratch/rg18646/DD4HEP/lcgeo /scratch/rg18646/DD4HEP/lcgeo /scratch/rg18646/DD4HEP/lcgeo/build /scratch/rg18646/DD4HEP/lcgeo/build /scratch/rg18646/DD4HEP/lcgeo/build/CMakeFiles/ContinuousBuild.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ContinuousBuild.dir/depend

