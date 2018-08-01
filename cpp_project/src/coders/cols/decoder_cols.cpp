
#include "decoder_cols.h"

#include "assert.h"


void DecoderCols::decodeDataRows(){
    std::vector<std::vector<std::string>> columns;
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
        std::cout << "decode column_index " << column_index << std::endl;
        dataset.setColumn(column_index);
        std::vector<std::string> column = decodeColumn();
        columns.push_back(column);
    }
    transposeMatrix(columns, total_columns);
}

std::vector<std::string> DecoderCols::decodeColumn(){
    if (column_index == 0) {
        return decodeTimeDeltaColumn();
    }
    else {
        if (Constants::MASK_MODE) {
            decodeDataColumnNoDataMask();
        }
        return decodeDataColumn();
    }
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
        int value_int = std::stoi(value);
        time_delta_vector.push_back(value_int);
    }
    return column;
}

void DecoderCols::decodeDataColumnNoDataMask() {
    int row_index = 0;
    while (row_index < data_rows_count){
        burst_is_no_data = decodeBool();
        burst_length = decodeInt(Constants::MASK_BITS) + 1; // 1<= burst_length <= Constants::MASK_MAX_SIZE
        std::cout << "decode burst_length = " << burst_length << std::endl;
        burst_is_no_data_vector.push_back(burst_is_no_data);
        burst_length_vector.push_back(burst_length);
        row_index += burst_length;
    }
    assert(row_index == data_rows_count);
    current_index = 0;
    burst_is_no_data = burst_is_no_data_vector.at(current_index);
    burst_length = burst_length_vector.at(current_index);
    std::cout << "END decodeDataColumnNoDataMask" << std::endl;
}

bool DecoderCols::isNoData(){
    if (burst_length == 0){
        current_index++;
        burst_is_no_data = burst_is_no_data_vector.at(current_index);
        burst_length = burst_length_vector.at(current_index);
    }
    burst_length--;
    return burst_is_no_data;
}

void DecoderCols::transposeMatrix(std::vector<std::vector<std::string>> columns, int total_columns){
    for(int row_index_ = 0; row_index_ < data_rows_count; row_index_++){
        std::vector<std::string> row;
        for(int column_index_ = 0; column_index_ < total_columns; column_index_++) {
            row.push_back(columns[column_index_][row_index_]);
        }
        output_csv.writeRowDecoder(row);
    }
}
