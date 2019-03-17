
#include "coder_cols.h"

#include "assert.h"
#include "string_utils.h"
#include "mask_coder.h"
#include "time_delta_coder.h"
#include "coder_utils.h"

void CoderCols::codeDataRows(){
    int total_columns = dataset->data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
    #if COUT
        std::cout << "ccode column_index " << column_index << std::endl;
    #endif
        dataset->setColumn(column_index);
        codeColumn();
    }
}

void CoderCols::codeColumn() {
    if (column_index == 0) {
        dataset->setMode("DATA");
        time_delta_vector = TimeDeltaCoder::code(this);
        return;
    }
#if MASK_MODE
    dataset->setMode("MASK");
//    std::cout << "MaskCoder::code();" << std::endl;
    total_data_rows = MaskCoder::code(this, column_index);
#endif

    dataset->setMode("DATA");
    std::cout << "codeDataColumn();" << std::endl;
    codeDataColumn();
}

void CoderCols::codeDataColumn(){
    this->codeColumnBefore();

    row_index = 0;
    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        this->codeColumnWhile(csv_value);
        row_index++;
    }
    this->codeColumnAfter();
}
