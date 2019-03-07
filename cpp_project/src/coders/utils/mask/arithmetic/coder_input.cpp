
#include "coder_input.h"
#include "constants.h"
#include <iostream>

CoderInput::CoderInput(CSVReader* input_csv_, int column_index){
    input_csv = input_csv_;
    input_csv->goToFirstDataRow(column_index);
    total_data_rows = 0;
    total_rows = 0;
}

int CoderInput::getByte(){
    int value = -1;
    if (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        if (Constants::isNoData(csv_value))
            value = 1;
        else {
            total_data_rows++;
            value = 0;
        }
    }
    std::cout << "[" << total_rows << "] >>>>>>>>>>>>>>>>>>> CoderInput = " << value << std::endl;
    total_rows++;
    return value;
}
