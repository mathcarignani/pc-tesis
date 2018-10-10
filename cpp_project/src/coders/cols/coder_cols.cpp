
#include "coder_cols.h"

#include "assert.h"
#include "string_utils.h"
#include "mask_coder.h"

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

void CoderCols::goToFirstDataRow() {
    row_index = 0;
    input_csv->goToFirstDataRow();
}

void CoderCols::codeColumn() {
    if (column_index == 0) {
        codeTimeDeltaColumn();
        return;
    }
#if MASK_MODE
    total_data_rows = MaskCoder::code(this, dataset, input_csv, column_index);
#endif
    codeDataColumn();
}

//
// TODO: use a more appropriate lossless compression schema for coding the time delta column.
//
void CoderCols::codeTimeDeltaColumn(){
    dataset->setMaskMode(false);

    goToFirstDataRow();
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readLineCSVWithIndex(column_index);
        codeValueRaw(csv_value); // same as CoderBasic

        // add int value to the time_delta_vector
        int csv_value_int = StringUtils::stringToInt(csv_value);
        time_delta_vector.push_back(csv_value_int);
        row_index++;
    }
}

void CoderCols::codeDataColumn(){
    dataset->setMaskMode(false);

    this->codeColumnBefore();

    goToFirstDataRow();
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readLineCSVWithIndex(column_index);
        this->codeColumnWhile(csv_value);
        row_index++;
    }

    this->codeColumnAfter();
}