
#include "coder_ca.h"
#include "conversor.h"

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

void CoderCA::codeColumnWhile(std::string csv_value){
    delta_sum += time_delta_vector[row_index]; // >= 0
#if MASK_MODE
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
#endif
    processValue(csv_value);
    delta_sum = 0;
}

void CoderCA::codeColumnAfter(){
    codeWindow();
}


void CoderCA::processValue(std::string x){
#if !MASK_MODE
    if (Constants::isNoData(x)){
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

    int x_int = Conversor::stringToInt(x);

    if (window->isEmpty()){
        if (window->nan_window){ // this condition can only be true on the first iteration
            codeValueAndCreateNonNanWindow(x, x_int);
            return;
        }

        if (delta_sum == 0) {
            codeValueAndCreateNonNanWindow(x, x_int);
        }
        else {
            window->setWindow(delta_sum, x_int, x);
        }
        return;
    }

    if (window->isFull()){
        codeWindow();
        codeValueAndCreateNonNanWindow(x, x_int);
        return;
    }

#if !MASK_MODE
    if (window->nan_window){
        codeWindow(); // code nan window
        codeValueAndCreateNonNanWindow(x, x_int);
        return;
    }
#endif

    if (delta_sum == 0 || not window->conditionHolds(delta_sum, x_int, x)){
        codeWindow(); // code non-nan window
        codeValueAndCreateNonNanWindow(x, x_int);
    }
}

void CoderCA::codeValueAndCreateNonNanWindow(std::string x, int x_int){
    codeWindow(1, x);
    window->createNonNanWindow(x, x_int);
}

void CoderCA::codeWindow(){
    codeWindow(window->length, window->constant_value);
}

void CoderCA::codeWindow(int window_length, std::string window_value){
    if (window_length == 0) { return; }
    codeInt(window_length - 1, window->window_size_bit_length);
    codeValueRaw(window_value);
}
