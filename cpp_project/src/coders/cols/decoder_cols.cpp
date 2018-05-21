
#include "decoder_cols.h"

#include <vector>

void DecoderCols::decodeDataRows(){
    std::vector<std::vector<std::string>> columns;
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
        std::cout << "CPP decode column_index " << column_index << std::endl;
        dataset.setColumn(column_index);
        std::vector<std::string> column = decodeColumn();
        columns.push_back(column);
    }

    // transpose matrix
    for(int row_index; row_index < data_rows_count; row_index++){
        std::vector<std::string> row;
        for(column_index = 0; column_index < total_columns; column_index++) {
            row.push_back(columns[column_index][row_index]);
        }
        output_csv.writeRowDecoder(row);
    }
}
