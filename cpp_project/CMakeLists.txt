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

set(CODER_HEADER_HEAD_DIR include/coders/header)
set(CODER_HEADER_SRC_DIR src/coders/header)

set(CODER_BASE_HEAD_DIR include/coders)
set(CODER_BASE_SRC_DIR src/coders)

set(CODER_COLS_HEAD_DIR include/coders/cols)
set(CODER_COLS_SRC_DIR src/coders/cols)

set(CODER_BASIC_HEAD_DIR include/coders/basic)
set(CODER_BASIC_SRC_DIR src/coders/basic)

set(CODER_PCA_HEAD_DIR include/coders/pca)
set(CODER_PCA_SRC_DIR src/coders/pca)

set(CODER_HEAD_DIRS ${CODER_HEADER_HEAD_DIR} ${CODER_BASE_HEAD_DIR} ${CODER_COLS_HEAD_DIR} ${CODER_BASIC_HEAD_DIR} ${CODER_PCA_HEAD_DIR})
set(CODER_STR_DIRS ${CODER_HEADER_SRC_DIR} ${CODER_BASE_SRC_DIR} ${CODER_COLS_SRC_DIR} ${CODER_BASIC_SRC_DIR} ${CODER_PCA_SRC_DIR})

set(BIT_STREAM_HEAD_DIR include/file_utils/bit_stream)
set(BIT_STREAM_SRC_DIR src/file_utils/bit_stream)

set(TEXT_HEAD_DIR include/file_utils/text)
set(TEXT_SRC_DIR src/file_utils/text)

set(CSV_HEAD_DIR include/file_utils/csv)
set(CSV_SRC_DIR src/file_utils/csv)

set(DATASET_HEAD_DIR include/dataset)
set(DATASET_SRC_DIR src/dataset)

set(HEAD_DIRS include ${BIT_STREAM_HEAD_DIR} ${TEXT_HEAD_DIR} ${CSV_HEAD_DIR} ${CODER_HEAD_DIRS} ${DATASET_HEAD_DIR})
set(SRC_DIRS src ${BIT_STREAM_SRC_DIR} ${TEXT_SRC_DIR} ${CSV_SRC_DIR} ${CODER_STR_DIRS} ${DATASET_SRC_DIR})
include_directories(${HEAD_DIRS} ${SRC_DIR})

### FILE UTILS BEGIN ###################################################################################################
set(BIT_STREAM_HEAD_FILES ${BIT_STREAM_HEAD_DIR}/bit_stream_reader.h ${BIT_STREAM_HEAD_DIR}/bit_stream_writer.h ${BIT_STREAM_HEAD_DIR}/bit_stream_utils.h)
set(BIT_STREAM_SRC_FILES ${BIT_STREAM_SRC_DIR}/bit_stream_reader.cpp ${BIT_STREAM_SRC_DIR}/bit_stream_writer.cpp ${BIT_STREAM_SRC_DIR}/bit_stream_utils.cpp)

set(TEXT_HEAD_FILES ${TEXT_HEAD_DIR}/text_reader.h ${TEXT_HEAD_DIR}/text_utils.h)
set(TEXT_SRC_FILES ${TEXT_SRC_DIR}/text_reader.cpp ${TEXT_SRC_DIR}/text_utils.cpp)

set(CSV_HEAD_FILES ${CSV_HEAD_DIR}/csv_reader.h ${CSV_HEAD_DIR}/csv_utils.h ${CSV_HEAD_DIR}/csv_writer.h)
set(CSV_SRC_FILES ${CSV_SRC_DIR}/csv_reader.cpp ${CSV_SRC_DIR}/csv_utils.cpp ${CSV_SRC_DIR}/csv_writer.cpp)

set(FILE_UTILS_HEAD_FILES ${BIT_STREAM_HEAD_FILES} ${TEXT_HEAD_FILES} ${CSV_HEAD_FILES})
set(FILE_UTILS_SRC_FILES ${BIT_STREAM_SRC_FILES} ${TEXT_SRC_FILES} ${CSV_SRC_FILES})
### FILE UTILS END #####################################################################################################

### DATASET BEGIN ######################################################################################################
set(DATASET_HEAD_FILES ${DATASET_HEAD_DIR}/range.h ${DATASET_HEAD_DIR}/column_code.h ${DATASET_HEAD_DIR}/dataset.h ${DATASET_HEAD_DIR}/dataset_utils.h)
set(DATASET_SRC_FILES ${DATASET_SRC_DIR}/column_code.cpp ${DATASET_SRC_DIR}/dataset.cpp ${DATASET_SRC_DIR}/dataset_utils.cpp)
### DATASET END ########################################################################################################

### CODERS BEGIN #######################################################################################################
set(CODER_HEADER_HEAD_FILES ${CODER_HEADER_HEAD_DIR}/header_utils.h ${CODER_HEADER_HEAD_DIR}/header_coder.h ${CODER_HEADER_HEAD_DIR}/header_decoder.h)
set(CODER_HEADER_SRC_FILES ${CODER_HEADER_SRC_DIR}/header_coder.cpp ${CODER_HEADER_SRC_DIR}/header_decoder.cpp)

set(CODER_BASE_HEAD_FILES ${CODER_BASE_HEAD_DIR}/coder_base.h ${CODER_BASE_HEAD_DIR}/decoder_base.h)
set(CODER_BASE_SRC_FILES ${CODER_BASE_SRC_DIR}/coder_base.cpp ${CODER_BASE_SRC_DIR}/decoder_base.cpp)

set(CODER_COLS_HEAD_FILES ${CODER_COLS_HEAD_DIR}/coder_cols.h ${CODER_COLS_HEAD_DIR}/decoder_cols.h)
set(CODER_COLS_SRC_FILES ${CODER_COLS_SRC_DIR}/coder_cols.cpp ${CODER_COLS_SRC_DIR}/decoder_cols.cpp)

set(CODER_BASIC_HEAD_FILES ${CODER_BASIC_HEAD_DIR}/coder_basic.h ${CODER_BASIC_HEAD_DIR}/decoder_basic.h)
set(CODER_BASIC_SRC_FILES ${CODER_BASIC_SRC_DIR}/coder_basic.cpp ${CODER_BASIC_SRC_DIR}/decoder_basic.cpp)

set(CODER_PCA_HEAD_FILES ${CODER_PCA_HEAD_DIR}/coder_pca.h ${CODER_PCA_HEAD_DIR}/decoder_pca.h)
set(CODER_PCA_SRC_FILES ${CODER_PCA_SRC_DIR}/coder_pca.cpp ${CODER_PCA_SRC_DIR}/decoder_pca.cpp)

set(CODER_HEAD_FILES ${CODER_HEADER_HEAD_FILES} ${CODER_BASE_HEAD_FILES} ${DATASET_HEAD_FILES} ${CODER_COLS_HEAD_FILES} ${CODER_BASIC_HEAD_FILES} ${CODER_PCA_HEAD_FILES})
set(CODER_SRC_FILES ${CODER_HEADER_SRC_FILES} ${CODER_BASE_SRC_FILES} ${DATASET_SRC_FILES} ${CODER_COLS_SRC_FILES} ${CODER_BASIC_SRC_FILES} ${CODER_PCA_SRC_FILES})
### CODERS END #########################################################################################################

set(OTHER_HEAD_FILES1 include/string_utils.h include/datetime_utils.h include/vector_utils.h)
set(OTHER_SRC_FILES1 src/string_utils.cpp src/datetime_utils.cpp )

set(OTHER_HEAD_FILES2 include/scripts.h include/tests.h)
set(OTHER_SRC_FILES2 src/scripts.cpp src/tests.cpp)

set(HEAD_FILES ${OTHER_HEAD_FILES1} ${FILE_UTILS_HEAD_FILES} ${DATASET_HEAD_FILES} ${CODER_HEAD_FILES} ${OTHER_HEAD_FILES2})
set(SOURCE_FILES ${OTHER_SRC_FILES1} ${FILE_UTILS_SRC_FILES} ${CODER_SRC_FILES} ${OTHER_SRC_FILES2})

add_executable(cpp_project ${HEAD_FILES} ${SOURCE_FILES} main.cpp)
