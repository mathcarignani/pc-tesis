
#include "coder_cols.h"

#include "assert.h"
#include "string_utils.h"

void CoderCols::codeDataRows(){
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
    #if COUT
        std::cout << "code column_index " << column_index << std::endl;
    #endif
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
        return;
    }
#if MASK_MODE
    total_data_rows = codeDataColumnNoDataMask();
#endif
    codeDataColumn();
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
        int csv_value_int = StringUtils::stringToInt(csv_value);
        time_delta_vector.push_back(csv_value_int);
        row_index++;
    }
}

#if MASK_MODE
int CoderCols::codeDataColumnNoDataMask(){
    dataset.setMaskMode(true);

    bool burst_is_no_data = false;
    int burst_length = 0; // <= Constants::MASK_MAX_SIZE
    int total_data_rows = 0;

    goToFirstDataRow();
    while (input_csv.continue_reading) {
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        bool no_data = Constants::isNoData(csv_value);
        if (row_index == 0){
            burst_is_no_data = no_data;
            burst_length = 1;
        }
        else if (no_data != burst_is_no_data || burst_length == Constants::MASK_MAX_SIZE){
            total_data_rows += codeBurst(burst_is_no_data, burst_length);
            burst_is_no_data = no_data;
            burst_length = 1;
        }
        else {
            burst_length++;
        }
        row_index++;
    }
    assert(burst_length > 0);
    total_data_rows += codeBurst(burst_is_no_data, burst_length);
    return total_data_rows;
}

int CoderCols::codeBurst(bool burst_is_no_data, int burst_length){
    codeBool(burst_is_no_data);
    codeInt(burst_length - 1, Constants::MASK_BITS); // 1<= burst_length <= Constants::MASK_MAX_SIZE
    return ((burst_is_no_data) ? 0 : burst_length);
}
#endif

void CoderCols::codeDataColumn(){
    dataset.setMaskMode(false);

    this->codeColumnBefore();

    goToFirstDataRow();
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        this->codeColumnWhile(csv_value);
        row_index++;
    }

    this->codeColumnAfter();
}