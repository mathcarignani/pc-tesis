
#include "coder_ca.h"
#include "string_utils.h"

void CoderCA::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderCA::codeCoderParams(){
    codeCoderParameters(Constants::CODER_CA, window_size);
}

void CoderCA::codeColumnBefore(){
    int error_threshold = error_thresholds_vector.at(column_index);
    window = new CAWindow(window_size, error_threshold);
}

void CoderCA::codeColumnWhile(int value){
    delta_sum += time_delta_vector[row_index]; // >= 0
#if MASK_MODE
    if (Constants::isNoData(value)) { return; } // skip no_data
#endif
    processValue(value);
    delta_sum = 0;
}

void CoderCA::codeColumnAfter(){
    codeWindow();
}


void CoderCA::processValue(int value){
#if !MASK_MODE
    if (Constants::isNoData(value)){
        if (window->isFull()){
            codeWindow();
            window->createNanWindow();
        }
        else if (window->nan_window){
            if (window->isEmpty()){ // this condition can only be true on the first iteration
                window->createNanWindow();
            }
            else {
                window->increaseLength();
            }
        }
        else {
            codeWindow();
            window->createNanWindow();
        }
        return;
    }
#endif
    if (window->isEmpty()){
        if (window->nan_window){ // this condition can only be true on the first iteration
            codeValueAndCreateNonNanWindow(value);
            return;
        }

        if (delta_sum == 0) {
            codeValueAndCreateNonNanWindow(value);
        }
        else {
            window->setWindow(delta_sum, value);
        }
        return;
    }

    if (window->isFull()){
        codeWindow();
        codeValueAndCreateNonNanWindow(value);
        return;
    }

#if !MASK_MODE
    if (window->nan_window){
        codeWindow(); // code nan window
        codeValueAndCreateNonNanWindow(value);
        return;
    }
#endif

    if (delta_sum == 0 || not window->conditionHolds(delta_sum, value)){
        codeWindow(); // code non-nan window
        codeValueAndCreateNonNanWindow(value);
    }
}

void CoderCA::codeValueAndCreateNonNanWindow(int value){
    codeWindow(1, value);
    window->createNonNanWindow(value);
}

void CoderCA::codeWindow(){
    codeWindow(window->length, window->constant_value);
}

void CoderCA::codeWindow(int window_length, int window_value){
    if (window_length == 0) { return; }
    codeInt(window_length, window->window_size_bit_length);
    codeValueRaw(window_value);
}
