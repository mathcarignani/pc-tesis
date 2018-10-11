cmake_minimum_required(VERSION 3.9)
project(cpp_project)

set(CMAKE_CXX_STANDARD 11)

###############################

set(BENCHMARK_DIR external/benchmarkLinux)
set(PWLH_CONTROL_DIR external/benchmarkLinux/Algorithms/PWLH/Control)
set(DATA_DIR external/benchmarkLinux/DataManagementLayer/Data)
set(DYN_ARRAY_DIR external/benchmarkLinux/DataStructures/DynArray)
set(LINE_DIR external/benchmarkLinux/DataStructures/Line)
set(POLYGON_DIR external/benchmarkLinux/DataStructures/Polygon)
set(SF_DATA_DIR external/benchmarkLinux/Algorithms/SlideFilter/Data)

set(EXTERNAL_DIRS ${BENCHMARK_DIR} ${PWLH_CONTROL_DIR} ${DATA_DIR} ${DYN_ARRAY_DIR} ${LINE_DIR} ${POLYGON_DIR} ${SF_DATA_DIR})

set(CODERS_HEAD_DIR include/coders)
set(CODERS_SRC_DIR src/coders)

set(CODER_UTILS_HEAD_DIR include/coders/utils)
set(CODER_UTILS_SRC_DIR src/coders/utils)

set(CODER_HEADER_HEAD_DIR ${CODER_UTILS_HEAD_DIR}/header)
set(CODER_HEADER_SRC_DIR ${CODER_UTILS_SRC_DIR}/header)

set(CODER_MASK_HEAD_DIR ${CODER_UTILS_HEAD_DIR}/mask)
set(CODER_MASK_SRC_DIR ${CODER_UTILS_SRC_DIR}/mask)

set(CODER_BASE_HEAD_DIR ${CODERS_HEAD_DIR}/base)
set(CODER_BASE_SRC_DIR ${CODERS_SRC_DIR}/base)

set(CODER_COLS_HEAD_DIR ${CODERS_HEAD_DIR}/cols)
set(CODER_COLS_SRC_DIR ${CODERS_SRC_DIR}/cols)

set(CODER_BASIC_HEAD_DIR ${CODERS_HEAD_DIR}/basic)
set(CODER_BASIC_SRC_DIR ${CODERS_SRC_DIR}/basic)

set(CODER_PCA_HEAD_DIR ${CODERS_HEAD_DIR}/constant/pca)
set(CODER_PCA_SRC_DIR ${CODERS_SRC_DIR}/constant/pca)

set(CODER_APCA_HEAD_DIR ${CODERS_HEAD_DIR}/constant/apca)
set(CODER_APCA_SRC_DIR ${CODERS_SRC_DIR}/constant/apca)

set(CODER_PWLH_HEAD_DIR ${CODERS_HEAD_DIR}/linear/pwlh)
set(CODER_PWLH_SRC_DIR ${CODERS_SRC_DIR}/linear/pwlh)

set(CODER_SF_HEAD_DIR ${CODERS_HEAD_DIR}/linear/slide_filter)
set(CODER_SF_SRC_DIR ${CODERS_SRC_DIR}/linear/slide_filter)

set(CODER_CA_HEAD_DIR ${CODERS_HEAD_DIR}/linear/ca)
set(CODER_CA_SRC_DIR ${CODERS_SRC_DIR}/linear/ca)

set(CODER_FR_HEAD_DIR ${CODERS_HEAD_DIR}/linear/fr)
set(CODER_FR_SRC_DIR ${CODERS_SRC_DIR}/linear/fr)

set(CODER_GAMPS_HEAD_DIR ${CODERS_HEAD_DIR}/correlation/gamps)
set(CODER_GAMPS_SRC_DIR ${CODERS_SRC_DIR}/correlation/gamps)

set(CODER_HEAD_OTHER ${CODERS_HEAD_DIR} ${CODER_BASE_HEAD_DIR} ${CODER_COLS_HEAD_DIR} ${CODER_BASIC_HEAD_DIR})
set(CODER_HEAD_CONST ${CODER_PCA_HEAD_DIR} ${CODER_APCA_HEAD_DIR} ${CODER_PWLH_HEAD_DIR})
set(CODER_HEAD_LINEAR ${CODER_CA_HEAD_DIR} ${CODER_SF_HEAD_DIR} ${CODER_FR_HEAD_DIR} ${CODER_FR_HEAD_DIR})
set(CODER_HEAD_CORRELATION ${CODER_GAMPS_HEAD_DIR})
set(CODER_HEAD_UTILS ${CODER_UTILS_HEAD_DIR} ${CODER_HEADER_HEAD_DIR} ${CODER_MASK_HEAD_DIR})

set(CODER_SRC_OTHER ${CODERS_SRC_DIR} ${CODER_SRC_HEAD_DIR} ${CODER_BASE_SRC_DIR} ${CODER_COLS_SRC_DIR} ${CODER_BASIC_SRC_DIR})
set(CODER_SRC_CONST ${CODER_PCA_SRC_DIR} ${CODER_APCA_SRC_DIR} ${CODER_PWLH_SRC_DIR})
set(CODER_SRC_LINEAR ${CODER_CA_SRC_DIR} ${CODER_SF_SRC_DIR} ${CODER_FR_SRC_DIR})
set(CODER_SRC_CORRELATION ${CODER_GAMPS_SRC_DIR})
set(CODER_SRC_UTILS ${CODER_UTILS_SRC_DIR} ${CODER_HEADER_SRC_DIR} ${CODER_MASK_SRC_DIR})

set(CODER_HEAD_DIRS ${CODER_HEAD_OTHER} ${CODER_HEAD_CONST} ${CODER_HEAD_LINEAR} ${CODER_HEAD_CORRELATION} ${CODER_HEAD_UTILS})
set(CODER_SRC_DIRS ${CODER_SRC_OTHER} ${CODER_SRC_CONST} ${CODER_SRC_LINEAR} ${CODER_SRC_CORRELATION} ${CODER_SRC_UTILS})

set(FILE_UTILS_HEAD_DIR include/file_utils)

set(BIT_STREAM_HEAD_DIR include/file_utils/bit_stream)
set(BIT_STREAM_SRC_DIR src/file_utils/bit_stream)

set(TEXT_HEAD_DIR include/file_utils/text)
set(TEXT_SRC_DIR src/file_utils/text)

set(CSV_HEAD_DIR include/file_utils/csv)
set(CSV_SRC_DIR src/file_utils/csv)

set(DATASET_HEAD_DIR include/dataset)
set(DATASET_SRC_DIR src/dataset)

set(TESTS_HEAD_DIR include/tests)
set(TESTS_SRC_DIR src/tests)

set(HEAD_DIRS include ${FILE_UTILS_HEAD_DIR} ${BIT_STREAM_HEAD_DIR} ${TEXT_HEAD_DIR} ${CSV_HEAD_DIR} ${CODER_HEAD_DIRS} ${DATASET_HEAD_DIR} ${TESTS_HEAD_DIR})
set(SRC_DIRS src ${BIT_STREAM_SRC_DIR} ${TEXT_SRC_DIR} ${CSV_SRC_DIR} ${CODER_SRC_DIRS} ${DATASET_SRC_DIR} ${TESTS_SRC_DIR})
include_directories(${EXTERNAL_DIRS} ${HEAD_DIRS} ${SRC_DIR})

### EXTERNAL BEGIN #####################################################################################################
set(EXTERNAL_DATA_STRUCTURES_HEAD_FILES ${DYN_ARRAY_DIR}/DynArray.h ${LINE_DIR}/Line.h ${POLYGON_DIR}/CPolygon.h)
set(EXTERNAL_DATA_STRUCTURES_SRC_FILES ${DYN_ARRAY_DIR}/DynArray.cpp ${LINE_DIR}/Line.cpp ${POLYGON_DIR}/CPolygon.cpp)

set(EXTERNAL_HEAD_FILES ${BENCHMARK_DIR}/stdafx.h ${EXTERNAL_DATA_STRUCTURES_HEAD_FILES} ${DATA_DIR}/DataItem.h ${DATA_DIR}/DataStream.h ${PWLH_CONTROL_DIR}/LinearBucket.h ${SF_DATA_DIR}/SlideFiltersEntry.h)
set(EXTERNAL_SRC_FILES ${EXTERNAL_DATA_STRUCTURES_SRC_FILES} ${PWLH_CONTROL_DIR}/LinearBucket.cpp ${DATA_DIR}/DataStream.cpp)
### EXTERNAL END #######################################################################################################

### FILE UTILS BEGIN ###################################################################################################
set(BIT_STREAM_HEAD_FILES ${BIT_STREAM_HEAD_DIR}/bit_stream_reader.h ${BIT_STREAM_HEAD_DIR}/bit_stream_writer.h ${BIT_STREAM_HEAD_DIR}/bit_stream_utils.h)
set(BIT_STREAM_SRC_FILES ${BIT_STREAM_SRC_DIR}/bit_stream_reader.cpp ${BIT_STREAM_SRC_DIR}/bit_stream_writer.cpp ${BIT_STREAM_SRC_DIR}/bit_stream_utils.cpp)

set(TEXT_HEAD_FILES ${TEXT_HEAD_DIR}/text_reader.h ${TEXT_HEAD_DIR}/text_utils.h)
set(TEXT_SRC_FILES ${TEXT_SRC_DIR}/text_reader.cpp ${TEXT_SRC_DIR}/text_utils.cpp)

set(CSV_HEAD_FILES ${CSV_HEAD_DIR}/csv_reader.h ${CSV_HEAD_DIR}/csv_utils.h ${CSV_HEAD_DIR}/csv_writer.h)
set(CSV_SRC_FILES ${CSV_SRC_DIR}/csv_reader.cpp ${CSV_SRC_DIR}/csv_utils.cpp ${CSV_SRC_DIR}/csv_writer.cpp)

set(FILE_UTILS_HEAD_FILES ${FILE_UTILS_HEAD_DIR}/path.h ${BIT_STREAM_HEAD_FILES} ${TEXT_HEAD_FILES} ${CSV_HEAD_FILES})
set(FILE_UTILS_SRC_FILES ${BIT_STREAM_SRC_FILES} ${TEXT_SRC_FILES} ${CSV_SRC_FILES})
### FILE UTILS END #####################################################################################################

### DATASET BEGIN ######################################################################################################
set(DATASET_HEAD_FILES ${DATASET_HEAD_DIR}/range.h ${DATASET_HEAD_DIR}/column_code.h ${DATASET_HEAD_DIR}/dataset.h ${DATASET_HEAD_DIR}/dataset_utils.h)
set(DATASET_SRC_FILES ${DATASET_SRC_DIR}/column_code.cpp ${DATASET_SRC_DIR}/dataset.cpp ${DATASET_SRC_DIR}/dataset_utils.cpp)
### DATASET END ########################################################################################################

### CODERS BEGIN #######################################################################################################
set(CODER_HEADER_HEAD_FILES ${CODER_HEADER_HEAD_DIR}/header_utils.h ${CODER_HEADER_HEAD_DIR}/header_coder.h ${CODER_HEADER_HEAD_DIR}/header_decoder.h)
set(CODER_HEADER_SRC_FILES ${CODER_HEADER_SRC_DIR}/header_coder.cpp ${CODER_HEADER_SRC_DIR}/header_decoder.cpp)

set(CODER_MASK_HEAD_FILES ${CODER_MASK_HEAD_DIR}/mask.h ${CODER_MASK_HEAD_DIR}/mask_coder.h ${CODER_MASK_HEAD_DIR}/mask_decoder.h)
set(CODER_MASK_SRC_FILES ${CODER_MASK_SRC_DIR}/mask_coder.cpp ${CODER_MASK_SRC_DIR}/mask_decoder.cpp)

set(CODER_BASE_HEAD_FILES ${CODER_BASE_HEAD_DIR}/coder_base.h ${CODER_BASE_HEAD_DIR}/decoder_base.h)
set(CODER_BASE_SRC_FILES ${CODER_BASE_SRC_DIR}/coder_base.cpp ${CODER_BASE_SRC_DIR}/decoder_base.cpp)

set(CODER_COLS_HEAD_FILES ${CODER_COLS_HEAD_DIR}/coder_cols.h ${CODER_COLS_HEAD_DIR}/decoder_cols.h)
set(CODER_COLS_SRC_FILES ${CODER_COLS_SRC_DIR}/coder_cols.cpp ${CODER_COLS_SRC_DIR}/decoder_cols.cpp)

set(CODER_BASIC_HEAD_FILES ${CODER_BASIC_HEAD_DIR}/coder_basic.h ${CODER_BASIC_HEAD_DIR}/decoder_basic.h)
set(CODER_BASIC_SRC_FILES ${CODER_BASIC_SRC_DIR}/coder_basic.cpp ${CODER_BASIC_SRC_DIR}/decoder_basic.cpp)

set(CODER_PCA_HEAD_FILES ${CODER_PCA_HEAD_DIR}/pca_window.h ${CODER_PCA_HEAD_DIR}/coder_pca.h ${CODER_PCA_HEAD_DIR}/decoder_pca.h)
set(CODER_PCA_SRC_FILES ${CODER_PCA_SRC_DIR}/pca_window.cpp ${CODER_PCA_SRC_DIR}/coder_pca.cpp ${CODER_PCA_SRC_DIR}/decoder_pca.cpp)

set(CODER_APCA_HEAD_FILES ${CODER_APCA_HEAD_DIR}/apca_window.h ${CODER_APCA_HEAD_DIR}/coder_apca.h ${CODER_APCA_HEAD_DIR}/decoder_apca.h)
set(CODER_APCA_SRC_FILES ${CODER_APCA_SRC_DIR}/apca_window.cpp ${CODER_APCA_SRC_DIR}/coder_apca.cpp ${CODER_APCA_SRC_DIR}/decoder_apca.cpp)

set(CODER_PWLH_HEAD_FILES ${CODER_PWLH_HEAD_DIR}/pwlh_window.h ${CODER_PWLH_HEAD_DIR}/coder_pwlh.h ${CODER_PWLH_HEAD_DIR}/decoder_pwlh.h)
set(CODER_PWLH_SRC_FILES ${CODER_PWLH_SRC_DIR}/pwlh_window.cpp ${CODER_PWLH_SRC_DIR}/coder_pwlh.cpp ${CODER_PWLH_SRC_DIR}/decoder_pwlh.cpp)

set(CODER_SF_HEAD_FILES ${CODER_SF_HEAD_DIR}/slide_filter_window.h ${CODER_SF_HEAD_DIR}/coder_slide_filter.h ${CODER_SF_HEAD_DIR}/decoder_slide_filter.h)
set(CODER_SF_SRC_FILES ${CODER_SF_SRC_DIR}/slide_filter_window.cpp ${CODER_SF_SRC_DIR}/coder_slide_filter.cpp ${CODER_SF_SRC_DIR}/decoder_slide_filter.cpp)

set(CODER_CA_HEAD_FILES ${CODER_CA_HEAD_DIR}/ca_line.h ${CODER_CA_HEAD_DIR}/ca_window.h ${CODER_CA_HEAD_DIR}/coder_ca.h ${CODER_CA_HEAD_DIR}/decoder_ca.h)
set(CODER_CA_SRC_FILES ${CODER_CA_SRC_DIR}/ca_window.cpp ${CODER_CA_SRC_DIR}/coder_ca.cpp ${CODER_CA_SRC_DIR}/decoder_ca.cpp)

set(CODER_FR_HEAD_FILES ${CODER_FR_HEAD_DIR}/fr_window.h ${CODER_FR_HEAD_DIR}/coder_fr.h ${CODER_FR_HEAD_DIR}/decoder_fr.h)
set(CODER_FR_SRC_FILES ${CODER_FR_SRC_DIR}/fr_window.cpp ${CODER_FR_SRC_DIR}/coder_fr.cpp ${CODER_FR_SRC_DIR}/decoder_fr.cpp)

set(CODER_GAMPS_HEAD_FILES ${CODER_GAMPS_HEAD_DIR}/coder_gamps.h ${CODER_GAMPS_HEAD_DIR}/decoder_gamps.h)
set(CODER_GAMPS_SRC_FILES ${CODER_GAMPS_SRC_DIR}/coder_gamps.cpp ${CODER_GAMPS_SRC_DIR}/decoder_gamps.cpp)

set(CODER_HEAD_FILES0 ${CODERS_HEAD_DIR}/constants.h ${CODER_UTILS_HEAD_DIR}/coder_utils.h ${CODER_UTILS_HEAD_DIR}/column.h)
set(CODER_HEAD_FILES1 ${CODER_HEADER_HEAD_FILES} ${CODER_MASK_HEAD_FILES} ${CODER_BASE_HEAD_FILES} ${DATASET_HEAD_FILES} ${CODER_COLS_HEAD_FILES} ${CODER_BASIC_HEAD_FILES})
set(CODER_HEAD_FILES2 ${CODER_PCA_HEAD_FILES} ${CODER_APCA_HEAD_FILES} ${CODER_PWLH_HEAD_FILES} ${CODER_SF_HEAD_FILES})
set(CODER_HEAD_FILES3 ${CODER_SF_HEAD_FILES} ${CODER_CA_HEAD_FILES} ${CODER_FR_HEAD_FILES} ${CODER_GAMPS_HEAD_FILES})

set(CODER_SRC_FILES0 ${CODERS_SRC_DIR}/constants.cpp ${CODER_UTILS_SRC_DIR}/coder_utils.cpp)
set(CODER_SRC_FILES1 ${CODER_HEADER_SRC_FILES} ${CODER_MASK_SRC_FILES} ${CODER_BASE_SRC_FILES} ${DATASET_SRC_FILES} ${CODER_COLS_SRC_FILES} ${CODER_BASIC_SRC_FILES})
set(CODER_SRC_FILES2 ${CODER_PCA_SRC_FILES} ${CODER_APCA_SRC_FILES} ${CODER_PWLH_SRC_FILES} ${CODER_SF_SRC_FILES})
set(CODER_SRC_FILES3 ${CODER_SF_HEAD_FILES} ${CODER_CA_SRC_FILES} ${CODER_FR_SRC_FILES} ${CODER_GAMPS_SRC_FILES})

set(CODER_HEAD_FILES ${CODER_HEAD_FILES0} ${CODER_HEAD_FILES1} ${CODER_HEAD_FILES2} ${CODER_HEAD_FILES3})
set(CODER_SRC_FILES ${CODER_SRC_FILES0} ${CODER_SRC_FILES1} ${CODER_SRC_FILES2} ${CODER_SRC_FILES3})
### CODERS END #########################################################################################################

### TESTS BEGIN ########################################################################################################
set(TESTS_HEAD_FILES0 ${TESTS_HEAD_DIR}/tests_vector_utils.h ${TESTS_HEAD_DIR}/tests_math_utils.h ${TESTS_HEAD_DIR}/tests_string_utils.h)
set(TESTS_HEAD_FILES1 ${TESTS_HEAD_DIR}/tests_line.h)
set(TESTS_HEAD_FILES2 ${TESTS_HEAD_DIR}/tests_coders_utils.h ${TESTS_HEAD_DIR}/tests_coders.h ${TESTS_HEAD_DIR}/tests.h)

set(TESTS_SRC_FILES0 ${TESTS_SRC_DIR}/tests_vector_utils.cpp ${TESTS_SRC_DIR}/tests_math_utils.cpp ${TESTS_SRC_DIR}/tests_string_utils.cpp)
set(TESTS_SRC_FILES1 ${TESTS_SRC_DIR}/tests_line.cpp)
set(TESTS_SRC_FILES2 ${TESTS_SRC_DIR}/tests_coders_utils.cpp ${TESTS_SRC_DIR}/tests_coders.cpp ${TESTS_SRC_DIR}/tests.cpp)

set(TESTS_HEAD_FILES ${TESTS_HEAD_FILES0} ${TESTS_HEAD_FILES1} ${TESTS_HEAD_FILES2})
set(TESTS_SRC_FILES ${TESTS_SRC_FILES0} ${TESTS_SRC_FILES1} ${TESTS_SRC_FILES2})
### TESTS END ##########################################################################################################

set(OTHER_HEAD_FILES1 include/os_utils.h include/string_utils.h include/datetime_utils.h include/vector_utils.h)
set(OTHER_SRC_FILES1 src/os_utils.cpp src/string_utils.cpp src/math_utils.cpp src/datetime_utils.cpp )

set(OTHER_HEAD_FILES2 include/scripts.h)
set(OTHER_SRC_FILES2 src/scripts.cpp)

set(HEAD_FILES ${EXTERNAL_HEAD_FILES} ${OTHER_HEAD_FILES1} ${FILE_UTILS_HEAD_FILES} ${DATASET_HEAD_FILES} ${CODER_HEAD_FILES} ${OTHER_HEAD_FILES2} ${TESTS_HEAD_FILES})
set(SOURCE_FILES ${EXTERNAL_SRC_FILES} ${OTHER_SRC_FILES1} ${FILE_UTILS_SRC_FILES} ${CODER_SRC_FILES} ${OTHER_SRC_FILES2} ${TESTS_SRC_FILES})

add_executable(cpp_project ${HEAD_FILES} ${SOURCE_FILES} main.cpp)
