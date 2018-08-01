
#include "coder_apca.h"


void CoderAPCA::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderAPCA::codeColumnBefore(){
    window = createWindow();
}

void CoderAPCA::codeColumnWhile(std::string csv_value){
    if (!window.conditionHolds(csv_value)){
        codeWindow(window);
        window.addFirstValue(csv_value);
    }
}

void CoderAPCA::codeColumnAfter(){
    if (!window.isEmpty()){ codeWindow(window); }
}

APCAWindow CoderAPCA::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    return APCAWindow(max_window_size, error_threshold);
}

void CoderAPCA::codeWindow(APCAWindow & window){
    codeInt(window.length, window.max_window_size_bit_length);
    codeValueRaw(window.constant_value);
}
