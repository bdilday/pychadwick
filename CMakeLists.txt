
cmake_minimum_required(VERSION 3.0)
project(libchadwick)
set(CMAKE_VERBOSE_MAKEFILE on)

add_definitions(-DVERSION=\"0.7.X\")

file(GLOB CWLIB_SOURCES "pychadwicklib/src/cwlib/*c")
include_directories(pychadwicklib/src)

set(CWEVENT_SOURCES pychadwicklib/src/cwtools/cwevent.c pychadwicklib/src/cwtools/cwtools.c ${CWLIB_SOURCES})
add_library(cwevent SHARED ${CWEVENT_SOURCES})
install(TARGETS cwevent LIBRARY DESTINATION cwevent)
