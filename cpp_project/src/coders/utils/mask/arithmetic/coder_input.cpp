
#include "coder_input.h"
#include "constants.h"

CoderInput::CoderInput(CSVReader* input_csv_, int column_index){
    input_csv = input_csv_;
    input_csv->goToFirstDataRow(column_index);
    total_data_rows = 0;
}

int CoderInput::getByte(){
    if (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        if (Constants::isNoData(csv_value))
            return 1;
        else {
            total_data_rows++;
            return 0;
        }
    }
    return -1;
}
