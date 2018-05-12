
#include "coder_cols.h"
#include <iostream>

void CoderCols::codeDataRows() {
    for (column_index = 0; column_index < columns_count; column_index++) {
        std::cout << "code column_index" << column_index;
        codeColumn();
    }
}
