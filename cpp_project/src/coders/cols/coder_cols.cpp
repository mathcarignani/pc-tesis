
#include "coder_cols.h"


void CoderCols::codeDataRows() {
    int total_columns = dataset.data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
        std::cout << "code column_index " << column_index << std::endl;
        dataset.setColumn(column_index);
        codeColumn();
    }
}

void CoderCols::codeColumn(){
    row_index = 0;
    input_csv.goToLine(4); // first data row
    if (column_index == 0) { codeTimeDeltaColumn(); } else { codeDataColumn(); }
}

void CoderCols::codeTimeDeltaColumn(){
    // TODO: use a more appropriate lossless compression schema for coding the time delta column.
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        codeValueRaw(csv_value); // same as CoderBasic

        // add int value to the time_delta_vector
        int csv_value_int = std::stoi(csv_value);
        time_delta_vector.push_back(csv_value_int);

        row_index++;
    }
}

void CoderCols::codeDataColumn(){
    this->codeColumnBefore();
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        std::cout << "csv_value = " << csv_value << std::endl;
        this->codeColumnWhile(csv_value);
        row_index++;
    }
    this->codeColumnAfter();
}