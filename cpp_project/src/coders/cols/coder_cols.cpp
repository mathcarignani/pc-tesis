
#include "coder_cols.h"

#include "assert.h"

void CoderCols::codeDataRows(){
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
        std::cout << "code column_index " << column_index << std::endl;
        dataset.setColumn(column_index);
        codeColumn();
    }
}

void CoderCols::goToFirstDataRow() {
    row_index = 0;
    input_csv.goToLine(4); // first data row
}

void CoderCols::codeColumn() {
    if (column_index == 0) {
        codeTimeDeltaColumn();
    }
    else {
        if (MASK_MODE) {
            codeDataColumnNoDataMask();
        }
        codeDataColumn();
    }
}

//
// TODO: use a more appropriate lossless compression schema for coding the time delta column.
//
void CoderCols::codeTimeDeltaColumn(){
    dataset.setMaskMode(false);

    goToFirstDataRow();
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        codeValueRaw(csv_value); // same as CoderBasic

        // add int value to the time_delta_vector
        int csv_value_int = std::stoi(csv_value);
        time_delta_vector.push_back(csv_value_int);

        row_index++;
    }
}

void CoderCols::codeDataColumnNoDataMask(){
    dataset.setMaskMode(true);

    bool burst_is_no_data = false;
    int burst_length = 0; // <= Constants::MASK_MAX_SIZE

    goToFirstDataRow();
    int total = 0;
    while (input_csv.continue_reading) {
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        bool no_data = Constants::isNoData(csv_value);
        if (row_index == 0){
            burst_is_no_data = no_data;
            burst_length = 1;
        }
        else if (no_data != burst_is_no_data || burst_length == Constants::MASK_MAX_SIZE){
            codeBool(burst_is_no_data);
            codeInt(burst_length - 1, Constants::MASK_BITS); // 1<= burst_length <= Constants::MASK_MAX_SIZE
            total++;
            std::cout << "ccode burst_length = " << burst_length << std::endl;
            burst_is_no_data = no_data;
            burst_length = 1;
        }
        else {
            burst_length++;
        }
        row_index++;
    }
    assert(burst_length > 0);
    codeBool(burst_is_no_data);
    codeInt(burst_length - 1, Constants::MASK_BITS);
    total++;
    std::cout << "total bursts = " << total << std::endl;
    std::cout << "ccode burst_length = " << burst_length << std::endl;
}

void CoderCols::codeDataColumn(){
    dataset.setMaskMode(false);

    this->codeColumnBefore();

    goToFirstDataRow();
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
//        std::cout << "csv_value = " << csv_value << std::endl;
        this->codeColumnWhile(csv_value);
        row_index++;
    }

    this->codeColumnAfter();
}