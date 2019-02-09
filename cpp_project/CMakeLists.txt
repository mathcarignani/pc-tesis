cmake_minimum_required(VERSION 3.9)
project(cpp_project)

set(CMAKE_CXX_STANDARD 11)

###############################

set(BENCHMARK_DIR external/benchmarkLinux)
set(ALGORITHMS_DIR ${BENCHMARK_DIR}/Algorithms)
set(GAMPS_CONTROL_DIR ${ALGORITHMS_DIR}/GAMPS/Control)
set(GAMPS_DATA_DIR ${ALGORITHMS_DIR}/GAMPS/Data)
set(PWLH_CONTROL_DIR ${ALGORITHMS_DIR}/PWLH/Control)
set(SF_DATA_DIR ${ALGORITHMS_DIR}/SlideFilter/Data)
set(DATA_DIR ${BENCHMARK_DIR}/DataManagementLayer/Data)
set(DYN_ARRAY_DIR ${BENCHMARK_DIR}/DataStructures/DynArray)
set(LINE_DIR ${BENCHMARK_DIR}/DataStructures/Line)
set(POLYGON_DIR ${BENCHMARK_DIR}/DataStructures/Polygon)
set(GAMPS_DIRS ${GAMPS_CONTROL_DIR} ${GAMPS_DATA_DIR})

set(EXTERNAL_DIRS ${BENCHMARK_DIR} ${DATA_DIR} ${DYN_ARRAY_DIR} ${LINE_DIR} ${POLYGON_DIR} ${GAMPS_DIRS} ${PWLH_CONTROL_DIR} ${SF_DATA_DIR})

set(CODERS_H_DIR include/coders)
set(CODERS_SRC_DIR src/coders)

set(CODER_UTILS_H_DIR include/coders/utils)
set(CODER_UTILS_SRC_DIR src/coders/utils)

set(CODER_HER_H_DIR ${CODER_UTILS_H_DIR}/header)
set(CODER_HER_SRC_DIR ${CODER_UTILS_SRC_DIR}/header)

set(CODER_MASK_H_DIR ${CODER_UTILS_H_DIR}/mask)
set(CODER_MASK_SRC_DIR ${CODER_UTILS_SRC_DIR}/mask)

set(CODER_SIMPLE_MASK_H_DIR ${CODER_MASK_H_DIR}/simple)
set(CODER_SIMPLE_MASK_SRC_DIR ${CODER_MASK_SRC_DIR}/simple)

set(CODER_GOLOMB_MASK_H_DIR ${CODER_MASK_H_DIR}/golomb)
set(CODER_GOLOMB_MASK_SRC_DIR ${CODER_MASK_SRC_DIR}/golomb)

set(CODER_TIME_DELTA_H_DIR ${CODER_UTILS_H_DIR}/time_delta)
set(CODER_TIME_DELTA_SRC_DIR ${CODER_UTILS_SRC_DIR}/time_delta)

set(CODER_BASE_H_DIR ${CODERS_H_DIR}/base)
set(CODER_BASE_SRC_DIR ${CODERS_SRC_DIR}/base)

set(CODER_COLS_H_DIR ${CODERS_H_DIR}/cols)
set(CODER_COLS_SRC_DIR ${CODERS_SRC_DIR}/cols)

set(CODER_BASIC_H_DIR ${CODERS_H_DIR}/basic)
set(CODER_BASIC_SRC_DIR ${CODERS_SRC_DIR}/basic)

set(CODER_CONSTANT_H_DIR ${CODERS_H_DIR}/constant)
set(CODER_CONSTANT_SRC_DIR ${CODERS_SRC_DIR}/constant)

set(CODER_PCA_H_DIR ${CODER_CONSTANT_H_DIR}/pca)
set(CODER_PCA_SRC_DIR ${CODER_CONSTANT_SRC_DIR}/pca)

set(CODER_APCA_H_DIR ${CODER_CONSTANT_H_DIR}/apca)
set(CODER_APCA_SRC_DIR ${CODER_CONSTANT_SRC_DIR}/apca)

set(CODER_LINEAR_H_DIR ${CODERS_H_DIR}/linear)
set(CODER_LINEAR_SRC_DIR ${CODERS_SRC_DIR}/linear)

set(CODER_PWLH_H_DIR ${CODERS_H_DIR}/linear/pwlh)
set(CODER_PWLH_SRC_DIR ${CODERS_SRC_DIR}/linear/pwlh)

set(CODER_SF_H_DIR ${CODERS_H_DIR}/linear/slide_filter)
set(CODER_SF_SRC_DIR ${CODERS_SRC_DIR}/linear/slide_filter)

set(CODER_CA_H_DIR ${CODERS_H_DIR}/linear/ca)
set(CODER_CA_SRC_DIR ${CODERS_SRC_DIR}/linear/ca)

set(CODER_FR_H_DIR ${CODERS_H_DIR}/linear/fr)
set(CODER_FR_SRC_DIR ${CODERS_SRC_DIR}/linear/fr)

set(CODER_GAMPS_H_DIR ${CODERS_H_DIR}/correlation/gamps)
set(CODER_GAMPS_SRC_DIR ${CODERS_SRC_DIR}/correlation/gamps)

set(CODER_H_OTHER ${CODERS_H_DIR} ${CODER_BASE_H_DIR} ${CODER_COLS_H_DIR} ${CODER_BASIC_H_DIR})
set(CODER_H_CONST ${CODER_CONSTANT_H_DIR} ${CODER_PCA_H_DIR} ${CODER_APCA_H_DIR} ${CODER_PWLH_H_DIR})
set(CODER_H_LINEAR ${CODER_LINEAR_H_DIR} ${CODER_CA_H_DIR} ${CODER_SF_H_DIR} ${CODER_FR_H_DIR} ${CODER_FR_H_DIR})
set(CODER_H_CORRELATION ${CODER_GAMPS_H_DIR})
set(CODER_H_UTILS_MASK ${CODER_MASK_H_DIR} ${CODER_SIMPLE_MASK_H_DIR} ${CODER_GOLOMB_MASK_H_DIR})
set(CODER_H_UTILS ${CODER_UTILS_H_DIR} ${CODER_HER_H_DIR} ${CODER_H_UTILS_MASK} ${CODER_TIME_DELTA_H_DIR})

set(CODER_SRC_OTHER ${CODERS_SRC_DIR} ${CODER_SRC_H_DIR} ${CODER_BASE_SRC_DIR} ${CODER_COLS_SRC_DIR} ${CODER_BASIC_SRC_DIR})
set(CODER_SRC_CONST ${CODER_PCA_SRC_DIR} ${CODER_APCA_SRC_DIR} ${CODER_PWLH_SRC_DIR})
set(CODER_SRC_LINEAR ${CODER_LINEAR_SRC_DIR} ${CODER_CA_SRC_DIR} ${CODER_SF_SRC_DIR} ${CODER_FR_SRC_DIR})
set(CODER_SRC_CORRELATION ${CODER_GAMPS_SRC_DIR})
set(CODER_SRC_UTILS_MASK ${CODER_MASK_SRC_DIR} ${CODER_SIMPLE_MASK_SRC_DIR} ${CODER_GOLOMB_MASK_SRC_DIR})
set(CODER_SRC_UTILS ${CODER_UTILS_SRC_DIR} ${CODER_HER_SRC_DIR} ${CODER_SRC_UTILS_MASK}  ${CODER_TIME_DELTA_SRC_DIR})

set(CODER_H_DIRS ${CODER_H_OTHER} ${CODER_H_CONST} ${CODER_H_LINEAR} ${CODER_H_CORRELATION} ${CODER_H_UTILS})
set(CODER_SRC_DIRS ${CODER_SRC_OTHER} ${CODER_SRC_CONST} ${CODER_SRC_LINEAR} ${CODER_SRC_CORRELATION} ${CODER_SRC_UTILS})

set(FILE_UTILS_H_DIR include/file_utils)

set(BIT_STREAM_H_DIR include/file_utils/bit_stream)
set(BIT_STREAM_SRC_DIR src/file_utils/bit_stream)

set(TEXT_H_DIR include/file_utils/text)
set(TEXT_SRC_DIR src/file_utils/text)

set(CSV_H_DIR include/file_utils/csv)
set(CSV_SRC_DIR src/file_utils/csv)

set(DATASET_H_DIR include/dataset)
set(DATASET_SRC_DIR src/dataset)

set(TESTS_H_DIR include/tests)
set(TESTS_SRC_DIR src/tests)

set(TESTS_UTILS_H_DIR include/tests/utils)
set(TESTS_UTILS_SRC_DIR src/tests/utils)

set(UTILS_H_DIR include/utils)
set(UTILS_SRC_DIR src/utils)

set(H_DIRS include ${FILE_UTILS_H_DIR} ${BIT_STREAM_H_DIR} ${TEXT_H_DIR} ${CSV_H_DIR} ${CODER_H_DIRS} ${DATASET_H_DIR} ${TESTS_H_DIR} ${UTILS_H_DIR} ${TESTS_UTILS_H_DIR})
set(SRC_DIRS src ${BIT_STREAM_SRC_DIR} ${TEXT_SRC_DIR} ${CSV_SRC_DIR} ${CODER_SRC_DIRS} ${DATASET_SRC_DIR} ${TESTS_SRC_DIR} ${UTILS_SRC_DIR} ${TESTS_UTILS_SRC_DIR})
include_directories(${EXTERNAL_DIRS} ${H_DIRS} ${SRC_DIR})

### EXTERNAL BEGIN #####################################################################################################
set(EXTERNAL_DATA_STRUCTURES_H_FILES ${DYN_ARRAY_DIR}/DynArray.h ${LINE_DIR}/Line.h ${POLYGON_DIR}/CPolygon.h)
set(EXTERNAL_DATA_STRUCTURES_SRC_FILES ${DYN_ARRAY_DIR}/DynArray.cpp ${LINE_DIR}/Line.cpp ${POLYGON_DIR}/CPolygon.cpp)

set(EXTERNAL_DATA_H_FILES ${DATA_DIR}/DataItem.h ${DATA_DIR}/DataStream.h ${DATA_DIR}/MultiDataStream.h ${DATA_DIR}/Output.h)
set(EXTERNAL_DATA_SRC_FILES ${DATA_DIR}/DataStream.cpp ${DATA_DIR}/MultiDataStream.cpp)

set(EXTERNAL_GAMPS_CONTROL_H_FILES ${GAMPS_CONTROL_DIR}/FacilityLocProb.h ${GAMPS_CONTROL_DIR}/GAMPS_Computation.h ${GAMPS_CONTROL_DIR}/gamps.h)
set(EXTERNAL_GAMPS_CONTROL_SRC_FILES ${GAMPS_CONTROL_DIR}/FacilityLocProb.cpp ${GAMPS_CONTROL_DIR}/GAMPS_Computation.cpp ${GAMPS_CONTROL_DIR}/gamps.cpp)

set(EXTERNAL_GAMPS_DATA_H_FILES ${GAMPS_DATA_DIR}/GAMPSInput.h ${GAMPS_DATA_DIR}/GAMPSOutput.h)
set(EXTERNAL_GAMPS_DATA_SRC_FILES ${GAMPS_DATA_DIR}/GAMPSInput.cpp ${GAMPS_DATA_DIR}/GAMPSOutput.cpp)

set(EXTERNAL_GAMPS_H_FILES ${EXTERNAL_GAMPS_CONTROL_H_FILES} ${EXTERNAL_GAMPS_DATA_H_FILES})
set(EXTERNAL_GAMPS_SRC_FILES ${EXTERNAL_GAMPS_CONTROL_SRC_FILES} ${EXTERNAL_GAMPS_DATA_SRC_FILES})

set(EXTERNAL_ALGORITHMS_H_FILES ${PWLH_CONTROL_DIR}/LinearBucket.h ${SF_DATA_DIR}/SlideFiltersEntry.h ${EXTERNAL_GAMPS_H_FILES} )
set(EXTERNAL_ALGORITHMS_SRC_FILES ${PWLH_CONTROL_DIR}/LinearBucket.cpp ${EXTERNAL_GAMPS_SRC_FILES})

set(EXTERNAL_H_FILES ${BENCHMARK_DIR}/stdafx.h ${EXTERNAL_DATA_STRUCTURES_H_FILES} ${EXTERNAL_DATA_H_FILES} ${EXTERNAL_ALGORITHMS_H_FILES})
set(EXTERNAL_SRC_FILES ${EXTERNAL_DATA_STRUCTURES_SRC_FILES} ${EXTERNAL_DATA_SRC_FILES} ${EXTERNAL_ALGORITHMS_SRC_FILES})
### EXTERNAL END #######################################################################################################

### FILE UTILS BEGIN ###################################################################################################
set(BIT_STREAM_H_FILES ${BIT_STREAM_H_DIR}/bit_stream_reader.h ${BIT_STREAM_H_DIR}/bit_stream_writer.h ${BIT_STREAM_H_DIR}/bit_stream_utils.h)
set(BIT_STREAM_SRC_FILES ${BIT_STREAM_SRC_DIR}/bit_stream_reader.cpp ${BIT_STREAM_SRC_DIR}/bit_stream_writer.cpp ${BIT_STREAM_SRC_DIR}/bit_stream_utils.cpp)

set(TEXT_H_FILES ${TEXT_H_DIR}/text_reader.h ${TEXT_H_DIR}/text_utils.h)
set(TEXT_SRC_FILES ${TEXT_SRC_DIR}/text_reader.cpp ${TEXT_SRC_DIR}/text_utils.cpp)

set(CSV_H_FILES ${CSV_H_DIR}/csv_reader.h ${CSV_H_DIR}/csv_utils.h ${CSV_H_DIR}/csv_writer.h)
set(CSV_SRC_FILES ${CSV_SRC_DIR}/csv_reader.cpp ${CSV_SRC_DIR}/csv_utils.cpp ${CSV_SRC_DIR}/csv_writer.cpp)

set(FILE_UTILS_H_FILES ${FILE_UTILS_H_DIR}/path.h ${BIT_STREAM_H_FILES} ${TEXT_H_FILES} ${CSV_H_FILES})
set(FILE_UTILS_SRC_FILES ${BIT_STREAM_SRC_FILES} ${TEXT_SRC_FILES} ${CSV_SRC_FILES})
### FILE UTILS END #####################################################################################################

### DATASET BEGIN ######################################################################################################
set(DATASET_H_FILES ${DATASET_H_DIR}/range.h ${DATASET_H_DIR}/column_code.h ${DATASET_H_DIR}/dataset.h ${DATASET_H_DIR}/dataset_utils.h)
set(DATASET_SRC_FILES ${DATASET_SRC_DIR}/column_code.cpp ${DATASET_SRC_DIR}/dataset.cpp ${DATASET_SRC_DIR}/dataset_utils.cpp)
### DATASET END ########################################################################################################

### CODERS BEGIN #######################################################################################################
set(CODER_HER_H_FILES ${CODER_HER_H_DIR}/header_utils.h ${CODER_HER_H_DIR}/header_coder.h ${CODER_HER_H_DIR}/header_decoder.h)
set(CODER_HER_SRC_FILES ${CODER_HER_SRC_DIR}/header_coder.cpp ${CODER_HER_SRC_DIR}/header_decoder.cpp)

set(CODER_MASK_H_FILES ${CODER_MASK_H_DIR}/burst.h ${CODER_MASK_H_DIR}/mask.h ${CODER_MASK_H_DIR}/mask_coder.h ${CODER_MASK_H_DIR}/mask_decoder.h)
set(CODER_MASK_SRC_FILES ${CODER_MASK_SRC_DIR}/mask.cpp ${CODER_MASK_SRC_DIR}/mask_coder.cpp ${CODER_MASK_SRC_DIR}/mask_decoder.cpp)

set(CODER_SIMPLE_MASK_H_FILES ${CODER_SIMPLE_MASK_H_DIR}/simple_mask_coder.h ${CODER_SIMPLE_MASK_H_DIR}/simple_mask_decoder.h)
set(CODER_SIMPLE_MASK_SRC_FILES ${CODER_SIMPLE_MASK_SRC_DIR}/simple_mask_coder.cpp ${CODER_SIMPLE_MASK_SRC_DIR}/simple_mask_decoder.cpp)

set(CODER_GOLOMB_MASK_H_FILES1 ${CODER_GOLOMB_MASK_H_DIR}/golomb_mask_coder.h ${CODER_GOLOMB_MASK_H_DIR}/golomb_mask_decoder.h)
set(CODER_GOLOMB_MASK_H_FILES2 ${CODER_GOLOMB_MASK_H_DIR}/golomb_coder.h ${CODER_GOLOMB_MASK_H_DIR}/golomb_decoder.h)
set(CODER_GOLOMB_MASK_H_FILES ${CODER_GOLOMB_MASK_H_FILES1} ${CODER_GOLOMB_MASK_H_FILES2})

set(CODER_GOLOMB_MASK_SRC_FILES1 ${CODER_GOLOMB_MASK_SRC_DIR}/golomb_mask_coder.cpp ${CODER_GOLOMB_MASK_SRC_DIR}/golomb_mask_decoder.cpp)
set(CODER_GOLOMB_MASK_SRC_FILES2 ${CODER_GOLOMB_MASK_SRC_DIR}/golomb_coder.cpp ${CODER_GOLOMB_MASK_SRC_DIR}/golomb_decoder.cpp)
set(CODER_GOLOMB_MASK_SRC_FILES ${CODER_GOLOMB_MASK_SRC_FILES1} ${CODER_GOLOMB_MASK_SRC_FILES2})

set(CODER_TIME_DELTA_H_FILES ${CODER_TIME_DELTA_H_DIR}/time_delta_coder.h ${CODER_TIME_DELTA_H_DIR}/time_delta_decoder.h)
set(CODER_TIME_DELTA_SRC_FILES ${CODER_TIME_DELTA_SRC_DIR}/time_delta_coder.cpp ${CODER_TIME_DELTA_SRC_DIR}/time_delta_decoder.cpp)

set(CODER_BASE_H_FILES ${CODER_BASE_H_DIR}/coder_base.h ${CODER_BASE_H_DIR}/decoder_base.h)
set(CODER_BASE_SRC_FILES ${CODER_BASE_SRC_DIR}/coder_base.cpp ${CODER_BASE_SRC_DIR}/decoder_base.cpp)

set(CODER_COLS_H_FILES ${CODER_COLS_H_DIR}/coder_cols.h ${CODER_COLS_H_DIR}/decoder_cols.h)
set(CODER_COLS_SRC_FILES ${CODER_COLS_SRC_DIR}/coder_cols.cpp ${CODER_COLS_SRC_DIR}/decoder_cols.cpp)

set(CODER_BASIC_H_FILES ${CODER_BASIC_H_DIR}/coder_basic.h ${CODER_BASIC_H_DIR}/decoder_basic.h)
set(CODER_BASIC_SRC_FILES ${CODER_BASIC_SRC_DIR}/coder_basic.cpp ${CODER_BASIC_SRC_DIR}/decoder_basic.cpp)

set(CODER_PCA_H_FILES ${CODER_PCA_H_DIR}/pca_window.h ${CODER_PCA_H_DIR}/coder_pca.h ${CODER_PCA_H_DIR}/decoder_pca.h)
set(CODER_PCA_SRC_FILES ${CODER_PCA_SRC_DIR}/pca_window.cpp ${CODER_PCA_SRC_DIR}/coder_pca.cpp ${CODER_PCA_SRC_DIR}/decoder_pca.cpp)

set(CODER_APCA_H_FILES ${CODER_APCA_H_DIR}/apca_window.h ${CODER_APCA_H_DIR}/coder_apca.h ${CODER_APCA_H_DIR}/decoder_apca.h)
set(CODER_APCA_SRC_FILES ${CODER_APCA_SRC_DIR}/apca_window.cpp ${CODER_APCA_SRC_DIR}/coder_apca.cpp ${CODER_APCA_SRC_DIR}/decoder_apca.cpp)

set(CODER_CONSTANT_H_FILES ${CODER_CONSTANT_H_DIR}/constant_coder_utils.h ${CODER_PCA_H_FILES} ${CODER_APCA_H_FILES})
set(CODER_CONSTANT_SRC_FILES ${CODER_PCA_SRC_FILES} ${CODER_APCA_SRC_FILES})

set(CODER_LINEAR_H_FILES ${CODER_LINEAR_H_DIR}/linear_coder_utils.h)
set(CODER_LINEAR_SRC_FILES ${CODER_LINEAR_SRC_DIR}/linear_coder_utils.cpp)

set(CODER_PWLH_H_CODER_PWLH_H_FILESFILES ${CODER_PWLH_H_DIR}/pwlh_window.h ${CODER_PWLH_H_DIR}/coder_pwlh.h ${CODER_PWLH_H_DIR}/decoder_pwlh.h)
set(CODER_PWLH_SRC_FILES ${CODER_PWLH_SRC_DIR}/pwlh_window.cpp ${CODER_PWLH_SRC_DIR}/coder_pwlh.cpp ${CODER_PWLH_SRC_DIR}/decoder_pwlh.cpp)

set(CODER_SF_H_FILES ${CODER_SF_H_DIR}/slide_filter_window.h ${CODER_SF_H_DIR}/coder_slide_filter.h ${CODER_SF_H_DIR}/decoder_slide_filter.h)
set(CODER_SF_SRC_FILES ${CODER_SF_SRC_DIR}/slide_filter_window.cpp ${CODER_SF_SRC_DIR}/coder_slide_filter.cpp ${CODER_SF_SRC_DIR}/decoder_slide_filter.cpp)

set(CODER_CA_H_FILES ${CODER_CA_H_DIR}/ca_window.h ${CODER_CA_H_DIR}/coder_ca.h ${CODER_CA_H_DIR}/decoder_ca.h)
set(CODER_CA_SRC_FILES ${CODER_CA_SRC_DIR}/ca_window.cpp ${CODER_CA_SRC_DIR}/coder_ca.cpp ${CODER_CA_SRC_DIR}/decoder_ca.cpp)

set(CODER_FR_H_FILES ${CODER_FR_H_DIR}/fr_window.h ${CODER_FR_H_DIR}/coder_fr.h ${CODER_FR_H_DIR}/decoder_fr.h)
set(CODER_FR_SRC_FILES ${CODER_FR_SRC_DIR}/fr_window.cpp ${CODER_FR_SRC_DIR}/coder_fr.cpp ${CODER_FR_SRC_DIR}/decoder_fr.cpp)

set(CODER_GAMPS_H_FILES ${CODER_GAMPS_H_DIR}/structs.h ${CODER_GAMPS_H_DIR}/coder_gamps.h ${CODER_GAMPS_H_DIR}/decoder_gamps.h)
set(CODER_GAMPS_SRC_FILES ${CODER_GAMPS_SRC_DIR}/structs.cpp ${CODER_GAMPS_SRC_DIR}/gamps_utils.cpp ${CODER_GAMPS_SRC_DIR}/coder_gamps.cpp ${CODER_GAMPS_SRC_DIR}/decoder_gamps.cpp)

set(CODER_H_FILES0 ${CODERS_H_DIR}/constants.h ${CODER_UTILS_H_DIR}/coder_utils.h ${CODER_UTILS_H_DIR}/column.h ${CODER_UTILS_H_DIR}/window.h)
set(CODER_H_FILES1 ${CODER_HER_H_FILES} ${CODER_MASK_H_FILES} ${CODER_SIMPLE_MASK_H_FILES} ${CODER_GOLOMB_MASK_H_FILES} ${DATASET_H_FILES})
set(CODER_H_FILES2 ${CODER_TIME_DELTA_H_FILES} ${CODER_BASE_H_FILES} ${CODER_COLS_H_FILES} ${CODER_BASIC_H_FILES})
set(CODER_H_FILES3 ${CODER_CONSTANT_H_FILES} ${CODER_LINEAR_H_FILES} ${CODER_PWLH_H_FILES} ${CODER_SF_H_FILES})
set(CODER_H_FILES4 ${CODER_SF_H_FILES} ${CODER_CA_H_FILES} ${CODER_FR_H_FILES} ${CODER_GAMPS_H_FILES})

set(CODER_SRC_FILES0 ${CODERS_SRC_DIR}/constants.cpp ${CODER_UTILS_SRC_DIR}/coder_utils.cpp)
set(CODER_SRC_FILES1 ${CODER_HER_SRC_FILES} ${CODER_MASK_SRC_FILES} ${CODER_SIMPLE_MASK_SRC_FILES} ${CODER_GOLOMB_MASK_SRC_FILES} ${DATASET_SRC_FILES})
set(CODER_SRC_FILES2 ${CODER_TIME_DELTA_SRC_FILES} ${CODER_BASE_SRC_FILES} ${CODER_COLS_SRC_FILES} ${CODER_BASIC_SRC_FILES})
set(CODER_SRC_FILES3 ${CODER_CONSTANT_SRC_FILES} ${CODER_LINEAR_SRC_FILES} ${CODER_PWLH_SRC_FILES} ${CODER_SF_SRC_FILES})
set(CODER_SRC_FILES4 ${CODER_SF_H_FILES} ${CODER_CA_SRC_FILES} ${CODER_FR_SRC_FILES} ${CODER_GAMPS_SRC_FILES})

set(CODER_H_FILES ${CODER_H_FILES0} ${CODER_H_FILES1} ${CODER_H_FILES2} ${CODER_H_FILES3} ${CODER_H_FILES4})
set(CODER_SRC_FILES ${CODER_SRC_FILES0} ${CODER_SRC_FILES1} ${CODER_SRC_FILES2} ${CODER_SRC_FILES3} ${CODER_SRC_FILES4})
### CODERS END #########################################################################################################

### TESTS BEGIN ########################################################################################################
set(TESTS_UTILS_H_FILES0 ${TESTS_UTILS_H_DIR}/tests_datetime_utils.h ${TESTS_UTILS_H_DIR}/tests_math_utils.h)
set(TESTS_UTILS_H_FILES1 ${TESTS_UTILS_H_DIR}/tests_string_utils.h ${TESTS_UTILS_H_DIR}/tests_vector_utils.h)

set(TESTS_UTILS_SRC_FILES0 ${TESTS_UTILS_SRC_DIR}/tests_datetime_utils.cpp ${TESTS_UTILS_SRC_DIR}/tests_math_utils.cpp)
set(TESTS_UTILS_SRC_FILES1 ${TESTS_UTILS_SRC_DIR}/tests_string_utils.cpp ${TESTS_UTILS_SRC_DIR}/tests_vector_utils.cpp)

set(TESTS_H_FILES0 ${TESTS_H_DIR}/tests_line.h ${TESTS_H_DIR}/tests_header_coder.h ${TESTS_H_DIR}/tests_utils.h)
set(TESTS_H_FILES1 ${TESTS_H_DIR}/tests_coders_utils.h ${TESTS_H_DIR}/tests_coders.h)
set(TESTS_H_FILES2 ${TESTS_H_DIR}/tests_dataset_utils.h ${TESTS_H_DIR}/tests_bit_stream.h ${TESTS_H_DIR}/tests.h)

set(TESTS_SRC_FILES0 ${TESTS_SRC_DIR}/tests_line.cpp ${TESTS_SRC_DIR}/tests_header_coder.cpp ${TESTS_SRC_DIR}/tests_utils.cpp)
set(TESTS_SRC_FILES1 ${TESTS_SRC_DIR}/tests_coders_utils.cpp ${TESTS_SRC_DIR}/tests_coders.cpp)
set(TESTS_SRC_FILES2 ${TESTS_SRC_DIR}/tests_dataset_utils.cpp ${TESTS_SRC_DIR}/tests_bit_stream.cpp ${TESTS_SRC_DIR}/tests.cpp)

set(TESTS_H_FILES ${TESTS_H_FILES0} ${TESTS_H_FILES1} ${TESTS_H_FILES2} ${TESTS_UTILS_H_FILES0} ${TESTS_UTILS_H_FILES1})
set(TESTS_SRC_FILES ${TESTS_SRC_FILES0} ${TESTS_SRC_FILES1} ${TESTS_SRC_FILES2} ${TESTS_UTILS_SRC_FILES0} ${TESTS_UTILS_SRC_FILES1})
### TESTS END ##########################################################################################################

### UTILS BEGIN ########################################################################################################
set(UTILS_H_FILES0 ${UTILS_H_DIR}/datetime_utils.h ${UTILS_H_DIR}/line_utils.h ${UTILS_H_DIR}/math_utils.h)
set(UTILS_H_FILES1 ${UTILS_H_DIR}/os_utils.h ${UTILS_H_DIR}/string_utils.h ${UTILS_H_DIR}/vector_utils.h)

set(UTILS_SRC_FILES0 ${UTILS_SRC_DIR}/datetime_utils.cpp ${UTILS_SRC_DIR}/line_utils.cpp ${UTILS_SRC_DIR}/math_utils.cpp)
set(UTILS_SRC_FILES1 ${UTILS_SRC_DIR}/os_utils.cpp ${UTILS_SRC_DIR}/string_utils.cpp)

set(UTILS_H_FILES ${UTILS_H_FILES0} ${UTILS_H_FILES1})
set(UTILS_SRC_FILES ${UTILS_SRC_FILES0} ${UTILS_SRC_FILES1})
### UTILS END ##########################################################################################################

set(OTHER_H_FILES include/scripts.h)
set(OTHER_SRC_FILES src/scripts.cpp)

set(H_FILES ${EXTERNAL_H_FILES} ${FILE_UTILS_H_FILES} ${UTILS_H_FILES} ${DATASET_H_FILES} ${CODER_H_FILES} ${OTHER_H_FILES} ${TESTS_H_FILES} )
set(SOURCE_FILES ${EXTERNAL_SRC_FILES} ${FILE_UTILS_SRC_FILES} ${UTILS_SRC_FILES} ${CODER_SRC_FILES} ${OTHER_SRC_FILES} ${TESTS_SRC_FILES})

add_executable(cpp_project ${H_FILES} ${SOURCE_FILES} main.cpp)
