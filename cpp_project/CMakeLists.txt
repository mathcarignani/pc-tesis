cmake_minimum_required(VERSION 3.9)
project(cpp_project)

set(CMAKE_CXX_STANDARD 11)

###############################

#set(HEADERS_DIR include)
#set(SOURCE_DIR src)
#
#AUX_SOURCE_DIRECTORY(${SOURCE_DIR} SOURCE_FILES)
#
#FILE(GLOB HEADER_FILES ${HEADERS_DIR}/*.h)
##FILE(GLOB SOURCE_FILES ${SOURCE_DIR}/*.cpp )
#
#
#include_directories(${SOURCE_DIR})
#
#
#add_executable(cpp_project ${HEADER_FILES} ${SOURCE_FILES})

#add_executable(cpp_project main.cpp external/minicsv.h include/csv_utils.h src/csv_utils.cpp)


set(EXT_DIR external)
set(HEAD_DIR include)
set(SRC_DIR src)
include_directories(${EXT_DIR} ${HEAD_DIR} ${SRC_DIR})

set(EXTERNAL_FILES external/minicsv.h)
set(HEAD_FILES include/operation_utils.h include/file_utils.h include/csv_utils.h include/bit_stream.h)
set(SOURCE_FILES src/operation_utils.cpp src/file_utils.cpp src/csv_utils.cpp src/bit_stream.cpp)
add_executable(cpp_project ${EXTERNAL_FILES} ${HEAD_FILES} ${SOURCE_FILES} main.cpp)


#include_directories(include/ src/ external/)
#set(SOURCE_FILES external/minicsv.h include/operation_utils.h include/file_utils.h include/csv_utils.h src/operation_utils.cpp src/csv_utils.cpp  main.cpp)
#add_executable(cpp_project ${SOURCE_FILES})
