
#include "decoder_cols.h"

#include "assert.h"
#include "string_utils.h"


void DecoderCols::decodeDataRows(){
    std::vector<std::vector<std::string>> columns;
    int total_columns = dataset->data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
    #if COUT
        std::cout << "decode column_index " << column_index << std::endl;
    #endif
        dataset->setColumn(column_index);
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
    mask = new Mask();

    int row_index = 0;
    while (row_index < data_rows_count){
        bool burst_is_no_data = decodeBool();
        int burst_length = decodeInt(Constants::MASK_BITS) + 1; // 1<= burst_length <= Constants::MASK_MAX_SIZE
        mask->add(burst_is_no_data, burst_length);
        row_index += burst_length;
    }
    assert(row_index == data_rows_count);
    total_data = mask->total_data;
    total_no_data = mask->total_no_data;
    reset();
}

bool DecoderCols::isNoData(){
    return mask->isNoData();
}

void DecoderCols::reset(){
    mask->reset();
}
#endif

void DecoderCols::transposeMatrix(std::vector<std::vector<std::string>> columns, int total_columns){
    for(int row_index_ = 0; row_index_ < data_rows_count; row_index_++){
        std::vector<std::string> row;
        for(int column_index_ = 0; column_index_ < total_columns; column_index_++) {
            row.push_back(columns[column_index_][row_index_]);
        }
        output_csv->writeRowDecoder(row);
    }
}

std::vector<int> DecoderCols::createXCoordsVector(){
    mask->reset();
    std::vector<int> result;
    int delta_sum = 1; // TODO: maybe this needs to be changed for coders other than Slide Filter
    for(int i=0; i < mask->total_data + mask->total_no_data; i++){
        delta_sum += time_delta_vector.at(i);
        if (mask->isNoData()) { continue; } // ignore these values
        result.push_back(delta_sum);
    }
    return result;
}
