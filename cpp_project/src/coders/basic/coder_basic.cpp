
#include "coder_basic.h"


void CoderBasic::codeColumn() {
    row_index = 0;
    input_csv.goToLine(4); // first data row
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        codeValueRaw(csv_value);
        row_index++;
    }
}
