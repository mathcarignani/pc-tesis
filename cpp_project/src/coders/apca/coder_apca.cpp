
#include "coder_apca.h"


void CoderAPCA::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderAPCA::codeColumn(){
    APCAWindow window = createWindow();
    row_index = 0;
    input_csv.goToLine(4); // first data row
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        if (!window.conditionHolds(csv_value)){
            codeWindow(window);
            window.addFirstValue(csv_value);
        }
        row_index++;
    }
    if (!window.isEmpty()){ codeWindow(window); }
}

APCAWindow CoderAPCA::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    return APCAWindow(max_window_size, error_threshold);
}

void CoderAPCA::codeWindow(APCAWindow & window){
    dataset.addBits(window.max_window_size_bit_length);
    output_file.pushInt(window.length, window.max_window_size_bit_length);
    codeValueRaw(window.constant_value);
}

std::string CoderAPCA::getInfo() {
    return "a";
}
