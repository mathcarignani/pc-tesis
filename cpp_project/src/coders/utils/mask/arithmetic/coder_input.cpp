
#include "coder_input.h"
#include "constants.h"
#include <iostream>

CoderInput::CoderInput(CSVReader* input_csv_, int column_index_){
    input_csv = input_csv_;
    std::cout << "column_index " << column_index_ << std::endl;
    input_csv->goToFirstDataRow(column_index);
    total_data_rows = 0;
    total_rows = 0;
    column_index = column_index_;
}

int CoderInput::getByte(){
    int value = -1;
    if (input_csv->continue_reading){
        value = getValue();
    }
    else {
        column_index++;
        std::cout << "column_index " << column_index << std::endl;
        if (column_index < 6){
            input_csv->goToFirstDataRow(column_index);
            value = getValue();
        }
    }
    std::cout << "[" << total_rows << "] >>>>>>>>>>>>>>>>>>> CoderInput = " << value << std::endl;
    total_rows++;
    return value;
}

int CoderInput::getValue(){
    std::string csv_value = input_csv->readNextValue2(column_index);
    std::cout << "csv_value = " << csv_value << std::endl;
    if (Constants::isNoData(csv_value))
        return 1;
    else {
        total_data_rows++;
        return 0;
    }
}