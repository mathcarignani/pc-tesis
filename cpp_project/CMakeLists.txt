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

set(CODER_BASE_HEAD_DIR include/coders)
set(CODER_BASE_SRC_DIR src/coders)

set(CODER_BASIC_HEAD_DIR include/coders/basic)
set(CODER_BASIC_SRC_DIR src/coders/basic)

set(CODER_HEAD_DIRS ${CODER_BASE_HEAD_DIR} ${CODER_BASIC_HEAD_DIR})
set(CODER_STR_DIRS ${CODER_BASE_SRC_DIR} ${CODER_BASIC_SRC_DIR})

set(BIT_STREAM_HEAD_DIR include/file_utils/bit_stream)
set(BIT_STREAM_SRC_DIR src/file_utils/bit_stream)

set(CSV_HEAD_DIR include/file_utils/csv)
set(CSV_SRC_DIR src/file_utils/csv)

set(HEAD_DIRS include ${BIT_STREAM_HEAD_DIR} ${CSV_HEAD_DIR} ${CODER_HEAD_DIRS})
set(SRC_DIRS src ${BIT_STREAM_SRC_DIR} ${CSV_SRC_DIR} ${CODER_STR_DIRS})
include_directories(${EXT_DIR} ${HEAD_DIRS} ${SRC_DIR})

set(CODER_BASE_HEAD_FILES ${CODER_BASE_HEAD_DIR}/coder_base.h ${CODER_BASE_HEAD_DIR}/header_utils.h) # ${CODER_BASE_HEAD_DIR}/decoder_base.h ${CODER_BASE_HEAD_DIR}/header_utils.h)
set(CODER_BASE_SRC_FILES ${CODER_BASE_SRC_DIR}/coder_base.cpp ${CODER_BASE_SRC_DIR}/header_utils.cpp) # ${CODER_BASE_SRC_DIR}/decoder_base.cpp ${CODER_BASE_SRC_DIR}/header_utils.cpp)

set(CODER_BASIC_HEAD_FILES ${CODER_BASIC_HEAD_DIR}/coder_basic.h) # ${CODER_BASIC_HEAD_DIR}/decoder_basic.h)
set(CODER_BASIC_SRC_FILES ${CODER_BASIC_SRC_DIR}/coder_basic.cpp) # ${CODER_BASIC_SRC_DIR}/decoder_basic.cpp)

set(CODER_HEAD_FILES ${CODER_BASE_HEAD_FILES} ${CODER_BASIC_HEAD_FILES})
set(CODER_SRC_FILES ${CODER_BASE_SRC_FILES} ${CODER_BASIC_SRC_FILES})

set(BIT_STREAM_HEAD_FILES ${BIT_STREAM_HEAD_DIR}/bit_stream_reader.h ${BIT_STREAM_HEAD_DIR}/bit_stream_writer.h)
set(BIT_STREAM_SRC_FILES ${BIT_STREAM_SRC_DIR}/bit_stream_reader.cpp ${BIT_STREAM_SRC_DIR}/bit_stream_writer.cpp)

set(CSV_HEAD_FILES ${CSV_HEAD_DIR}/csv_reader.h ${CSV_HEAD_DIR}/csv_utils.h ${CSV_HEAD_DIR}/csv_writer.h)
set(CSV_SRC_FILES ${CSV_SRC_DIR}/csv_reader.cpp ${CSV_SRC_DIR}/csv_utils.cpp ${CSV_SRC_DIR}/csv_writer.cpp)

set(EXTERNAL_FILES external/minicsv.h)
set(HEAD_FILES include/string_utils.h ${BIT_STREAM_HEAD_FILES} ${CSV_HEAD_FILES} ${CODER_HEAD_FILES})
set(SOURCE_FILES src/string_utils.cpp ${BIT_STREAM_SRC_FILES} ${CSV_SRC_FILES} ${CODER_SRC_FILES})

add_executable(cpp_project ${HEAD_FILES} ${SOURCE_FILES} main.cpp)


#include_directories(include/ src/ external/)
#set(SOURCE_FILES external/minicsv.h include/operation_utils.h include/file_utils.h include/csv_utils.h src/operation_utils.cpp src/csv_utils.cpp  main.cpp)
#add_executable(cpp_project ${SOURCE_FILES})
