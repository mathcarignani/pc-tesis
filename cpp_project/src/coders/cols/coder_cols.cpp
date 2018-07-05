
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
    this->codeColumnBefore();
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        this->codeColumnWhile(csv_value);
        row_index++;
    }
    this->codeColumnAfter();
}
