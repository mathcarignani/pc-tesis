
#include "coder_basic.h"


void CoderBasic::codeColumn() {
    row_index = 0;
    input_csv.goToLine(4); // first data row
    while (input_csv.continue_reading){
        std::vector<std::string> csv_row = input_csv.readLineCSV();
        std::string csv_value = csv_row[column_index];
        codeValueRaw(csv_value);
        row_index++;
    }
}

std::string CoderBasic::getInfo() {
    return "a";
}

