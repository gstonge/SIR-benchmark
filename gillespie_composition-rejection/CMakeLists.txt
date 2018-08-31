cmake_minimum_required(VERSION 3.1)

# Configure the project
#----------------------
project(propagation_simulation)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3" )
set(LIBRARY_OUTPUT_PATH lib/)
set(EXECUTABLE_OUTPUT_PATH bin/)

# Generate libraries
#-----------------------------
file( GLOB_RECURSE LIB_SOURCES lib/*.cpp)
file( GLOB_RECURSE LIB_HEADERS lib/*.hpp)
add_library( network ${LIB_SOURCES} ${LIB_HEADERS} )

# Generate file list for main files
#----------------------------------
#file( GLOB source_files src/* )

# Include libraries
#------------------
include_directories(lib/)
link_directories(lib/)

# Declare executables
#--------------------
add_executable( time_SIR src/time_SIR.cpp)
add_executable( threshold_SIR src/threshold_SIR.cpp)


# Link libraries
#---------------
target_link_libraries( time_SIR network)
target_link_libraries( threshold_SIR network)


