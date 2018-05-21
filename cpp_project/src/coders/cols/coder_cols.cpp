
#include "coder_cols.h"

#include "assert.h"


void CoderCols::codeDataRows() {
    std::cout << "dataset.columns_count " << dataset.data_columns_count << std::endl;
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
        std::cout << "code column_index " << column_index << std::endl;
        dataset.setColumn(column_index);
        codeColumn();
    }
}

//void CoderCols::raiseRangeError(int value){
//    std::cout << "RangeError" << std::endl;
//    std::cout << "Position = [row_index, col_index] = [" << row_index << "," << column_index << "]" << std::endl;
//    dataset.printRange();
//    std::cout << "value = " << value << std::endl;
//    assert(1==0);
//}
