
#include "coder_ca.h"

void CoderCA::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderCA::codeColumnBefore(){
    int error_threshold = error_thresholds_vector.at(column_index);
    window = CAWindow(max_window_size, error_threshold);
    max_window_size_bit_length = window.max_window_size_bit_length;
}

void CoderCA::codeColumnWhile(std::string csv_value){
    std::cout << "row_index = " << row_index << ", value = " << csv_value << std::endl;
    int x_delta = time_delta_vector[row_index]; // >= 0
    code(window, csv_value, x_delta);
}

void CoderCA::codeColumnAfter(){
    codeWindow(window.length, window.constant_value);
}

//
// NOTE: when force_code is true, the values of x and x_delta doesn't matter
//
// TODO: consider the x_delta == 0 case
//
void CoderCA::code(CAWindow & window, std::string x, int x_delta){
    bool no_data_x = x[0] == Constants::NO_DATA_CHAR;
    int x_int;
    if (!no_data_x) { x_int = std::stoi(x); }

    if (window.isEmpty()){
        std::cout << "window.isEmpty()" << std::endl;
        if (no_data_x){ // this condition can only be true on the first iteration
            window.createNanWindow();
            return;
        }
        // x is an integer
        if (window.nan_window){
            codeWindow(1, x);
            window.createNonNanWindow(x, x_int);
        }
        else { //
            window.updateValues(x, x_int, x_delta);
        }
        return;
    }
    if (window.isFull()){
        std::cout << "window.isFull()" << std::endl;
        codeWindow(window.length, window.constant_value);
        if (no_data_x){
            window.createNanWindow();
            return;
        }
        // x is an integer
        codeWindow(1, x);
        window.createNonNanWindow(x, x_int);
        return;
    }
    if (no_data_x){
        std::cout << "no_data_x" << std::endl;
        if (window.nan_window){
            window.updateLength(window.length + 1);
            return;
        }
        codeWindow(window.length, window.constant_value);
        window.createNanWindow();
        return;
    }
    // x is an integer
    if (window.nan_window){
        std::cout << "window.nan_window" << std::endl;
        codeWindow(window.length, window.constant_value); // code nan window
        codeWindow(1, x); // code single value window
        window.createNonNanWindow(x, x_int);
        return;
    }

    // non-nan window
    if (not window.conditionHolds(x_delta, x_int, x)){
        std::cout << "not window.conditionHolds(x_delta, x_int, x)" << std::endl;
        codeWindow(window.length, window.constant_value);
        codeWindow(1, x);
        window.createNonNanWindow(x, x_int);
    }
    else {
        std::cout << "else" << std::endl;
    }
}

void CoderCA::codeWindow(int window_length, std::string window_value){
    std::cout << "window.length = " << window_length << ", window.constant_value = " << window_value << std::endl;
    if (window_length == 0) { return; }
    dataset.addBits(max_window_size_bit_length);
    output_file.pushInt(window_length, max_window_size_bit_length);
    codeValueRaw(window_value);
}
