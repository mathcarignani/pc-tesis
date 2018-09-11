
#include "decoder_cols.h"

#include "assert.h"
#include "string_utils.h"


void DecoderCols::decodeDataRows(){
    std::vector<std::vector<std::string>> columns;
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
    #if COUT
        std::cout << "decode column_index " << column_index << std::endl;
    #endif
        dataset.setColumn(column_index);
        std::vector<std::string> column = decodeColumn();
        columns.push_back(column);
    }
    transposeMatrix(columns, total_columns);
}

std::vector<std::string> DecoderCols::decodeColumn(){
    if (column_index == 0) { return decodeTimeDeltaColumn(); }
    #if MASK_MODE
        decodeDataColumnNoDataMask();
    #endif
    return decodeDataColumn();
}

//
// TODO: use a more appropriate lossless compression schema for coding the time delta column.
//
std::vector<std::string> DecoderCols::decodeTimeDeltaColumn(){
    std::vector<std::string> column;
    for(int row_index = 0; row_index < data_rows_count; row_index++){
        std::string value = decodeValueRaw();
        column.push_back(value);

        // add int value to the time_delta_vector
        int value_int = StringUtils::stringToInt(value);
        time_delta_vector.push_back(value_int);
    }
    return column;
}

#if MASK_MODE
void DecoderCols::decodeDataColumnNoDataMask() {
    burst_is_no_data_vector.clear();
    burst_length_vector.clear();
    total_no_data = 0;
    total_data = 0;

    int row_index = 0;
    while (row_index < data_rows_count){
        burst_is_no_data = decodeBool();
        burst_length = decodeInt(Constants::MASK_BITS) + 1; // 1<= burst_length <= Constants::MASK_MAX_SIZE
//        std::cout << "decode burst_length = " << burst_length << std::endl;
        burst_is_no_data_vector.push_back(burst_is_no_data);
        burst_length_vector.push_back(burst_length);
        if (burst_is_no_data) { total_no_data += burst_length; } else { total_data += burst_length; }
        row_index += burst_length;
    }
    assert(row_index == data_rows_count);
    current_index = 0;
    burst_is_no_data = burst_is_no_data_vector.at(current_index);
    burst_length = burst_length_vector.at(current_index);
//    std::cout << "END decodeDataColumnNoDataMask" << std::endl;
}

bool DecoderCols::isNoData(){
//    std::cout << "current_index = " << current_index << std::endl;
//    std::cout << "size = " << burst_is_no_data_vector.size() << std::endl;
    if (burst_length == 0){
        current_index++;
        burst_is_no_data = burst_is_no_data_vector.at(current_index);
        burst_length = burst_length_vector.at(current_index);
//        std::cout << "bburst_length = " << burst_length << std::endl;
    }
    burst_length--;
    return burst_is_no_data;
}
#endif

void DecoderCols::transposeMatrix(std::vector<std::vector<std::string>> columns, int total_columns){
    for(int row_index_ = 0; row_index_ < data_rows_count; row_index_++){
        std::vector<std::string> row;
        for(int column_index_ = 0; column_index_ < total_columns; column_index_++) {
            row.push_back(columns[column_index_][row_index_]);
        }
        output_csv.writeRowDecoder(row);
    }
}
