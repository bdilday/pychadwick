
cmake_minimum_required(VERSION 3.0)
project(libchadwick)
set(CMAKE_VERBOSE_MAKEFILE on)

add_definitions(-DVERSION=\"0.7.X\")

file(GLOB CWLIB_SOURCES "src/pychadwicklib/cwlib/*c")
include_directories(src/pychadwicklib)

set(CWEVENT_SOURCES src/pychadwicklib/cwtools/cwevent.c src/pychadwicklib/cwtools/cwtools.c ${CWLIB_SOURCES})
add_library(cwevent SHARED ${CWEVENT_SOURCES})
install(TARGETS cwevent LIBRARY DESTINATION cwevent)
