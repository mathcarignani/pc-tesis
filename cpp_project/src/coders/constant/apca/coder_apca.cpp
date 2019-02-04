
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

void CoderAPCA::codeColumnWhile(int value){
    codeColumnWhile(this, window, value);
}

void CoderAPCA::codeColumnAfter(){
    codeColumnAfter(this, window);
}

void CoderAPCA::codeColumnWhile(CoderBase* coder, APCAWindow* window, int value){
#if MASK_MODE
    if (Constants::isNoData(value)) { return; } // skip no_data
#endif
    if (!window->conditionHolds(value)){
        codeWindow(coder, window);
        window->addFirstValue(value);
    }
}

void CoderAPCA::codeColumnAfter(CoderBase* coder, APCAWindow* window){
    if (!window->isEmpty()){ codeWindow(coder, window); }
}

void CoderAPCA::codeWindow(CoderBase* coder, APCAWindow* window){
    coder->codeInt(window->length, window->window_size_bit_length);
    coder->codeValueRaw(window->constant_value);
}
