
cmake_minimum_required(VERSION 3.0)
project(libchadwick)
set(CMAKE_VERBOSE_MAKEFILE on)

add_definitions(-DVERSION=\"0.7.X\")

file(GLOB CWLIB_SOURCES "src/cwlib/*c")
include_directories(src)

set(CWEVENT_SOURCES src/cwtools/cwevent.c src/cwtools/cwtools.c ${CWLIB_SOURCES})
add_library(cwevent SHARED ${CWEVENT_SOURCES})
