
#include "coder_basic.h"

void CoderBasic::codeDataRows(){
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
        std::cout << "code column_index " << column_index << std::endl;
        dataset.setColumn(column_index);
        codeColumn();
    }
}

void CoderBasic::codeColumn() {
    if (column_index == 0) {
        codeTimeDeltaColumn();
        return;
    }
    codeDataColumn();
}

void CoderBasic::codeColumnBefore() {}

void CoderBasic::codeColumnWhile(std::string csv_value){
    codeValueRaw(csv_value);
}

void CoderBasic::codeColumnAfter() {}