
#include "coder_apca.h"

void CoderAPCA::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderAPCA::codeCoderParams(){
    codeCoderParameters(Constants::CODER_APCA, window_size);
}

void CoderAPCA::codeColumnBefore(){
    int error_threshold = error_thresholds_vector.at(column_index);
    window = new APCAWindow(window_size, error_threshold);
}

void CoderAPCA::codeColumnWhile(std::string csv_value){
#if MASK_MODE
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
#endif
    if (!window->conditionHolds(csv_value)){
        codeWindow(window);
        window->addFirstValue(csv_value);
    }
}

void CoderAPCA::codeColumnAfter(){
    if (!window->isEmpty()){ codeWindow(window); }
}

void CoderAPCA::codeWindow(APCAWindow* window){
    codeInt(window->length, window->window_size_bit_length);
    codeValueRaw(window->constant_value);
}
