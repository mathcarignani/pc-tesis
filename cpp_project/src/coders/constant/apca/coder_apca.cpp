
#include "coder_apca.h"

void CoderAPCA::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_, bool mask_mode_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    mask_mode = mask_mode_;
}

void CoderAPCA::codeColumnBefore(){
    int error_threshold = error_thresholds_vector.at(column_index);
    window = new APCAWindow(window_size, error_threshold, mask_mode);
}

void CoderAPCA::codeColumnWhile(std::string csv_value){
if (mask_mode) {
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
}
    if (!window->conditionHolds(csv_value)){
        codeWindow(window);
        window->addFirstValue(csv_value);
    }
}

void CoderAPCA::codeColumnAfter(){
    if (!window->isEmpty()){ codeWindow(window); }
}

void CoderAPCA::codeWindow(APCAWindow* window){
    codeWindowLength((Window*) window);
    codeValueRaw(window->constant_value);
}
