
#include "decoder_cols.h"


void DecoderCols::decodeDataRows(){
    std::vector<std::vector<std::string>> columns;
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
        std::cout << "decode column_index " << column_index << std::endl;
        dataset.setColumn(column_index);
        std::vector<std::string> column = decodeColumnAux();
        columns.push_back(column);
    }
    transposeMatrix(columns, total_columns);
}

std::vector<std::string> DecoderCols::decodeColumnAux(){
    if (column_index == 0) { return decodeTimeDeltaColumn(); } else { return decodeColumn(); }
}

std::vector<std::string> DecoderCols::decodeTimeDeltaColumn(){
    // TODO: use a more appropriate lossless compression schema for coding the time delta column.
    std::vector<std::string> column;
    for(int row_index = 0; row_index < data_rows_count; row_index++){
        std::string value = decodeValueRaw();
        column.push_back(value);
    }
    return column;
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
