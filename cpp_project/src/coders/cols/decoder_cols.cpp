
#include "decoder_cols.h"
#include "assert.h"
#include "string_utils.h"
#include "mask_decoder.h"
#include "time_delta_decoder.h"

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
    if (column_index == 0) { return  TimeDeltaDecoder::decode(this); }
#if MASK_MODE
    mask = MaskDecoder::decode(this);
#endif
    return decodeDataColumn();
}

void DecoderCols::transposeMatrix(std::vector<std::vector<std::string>> columns, int total_columns){
    for(int row_index_ = 0; row_index_ < data_rows_count; row_index_++){
        std::vector<std::string> row;
        for(int column_index_ = 0; column_index_ < total_columns; column_index_++) {
            row.push_back(columns[column_index_][row_index_]);
        }
        output_csv->writeRowDecoder(row);
    }
}
