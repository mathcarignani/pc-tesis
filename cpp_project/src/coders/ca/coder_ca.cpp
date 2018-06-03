
#include "coder_ca.h"

void CoderCA::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderCA::codeColumn(){
    CAWindow window = createWindow();
    row_index = 0;
    input_csv.goToLine(4); // first data row
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
//        std::cout << row_index << " " << csv_value << std::endl;
        code(window, false, csv_value);
        row_index++;
    }
    code(window, true, "0"); // force code
}

CAWindow CoderCA::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    return CAWindow(max_window_size, error_threshold);
}

void CoderCA::code(CAWindow & window, bool force_code, std::string x){
    if (force_code){
        codeWindow(window, window.length, window.constant_value);
    }
    else if (window.isEmpty()){
        if (x[0] == 'N'){ // this condition can only be true on the first iteration
            window.createNanWindow();
        }
        else { // x is an integer
            int x_int = std::stoi(x);
            if (window.nan_window){
                codeWindow(window, 1, x);
                window.createNonNanWindow(x, x_int);
            }
            else {
                window.updateValues(x, x_int);
            }
        }
    }
    else if (window.isFull()){
        codeWindow(window, window.length, window.constant_value);
        if (x[0] == 'N'){
            window.createNanWindow();
        }
        else { // x is an integer
            int x_int = std::stoi(x);
            codeWindow(window, 1, x);
            window.createNonNanWindow(x, x_int);
        }
    }
    else if (x[0] == 'N'){
        if (window.nan_window){
            window.updateLength(window.length + 1);
        }
        else {
            codeWindow(window, window.length, window.constant_value);
            window.createNanWindow();
        }
    }
    else { // x is an integer
        int x_int = std::stoi(x);
        if (window.nan_window){
            codeWindow(window, window.length, window.constant_value); // code nan window
            codeWindow(window, 1, x); // code single value window
            window.createNonNanWindow(x, x_int);
        }
        else {
            CAPoint incoming_point = CAPoint(window.length + 1, x_int);
            if (not window.conditionHolds(incoming_point, x)){
//                std::cout << "(5.2)" << std::endl;
                codeWindow(window, window.length, window.constant_value);
                codeWindow(window, 1, x);
                window.createNonNanWindow(x, x_int);
            }
            else {
//                std::cout << "(5.3)" << std::endl;
            }
        }
    }
}

void CoderCA::codeWindow(CAWindow & window, int window_length, std::string window_value){
    if (window_length == 0) { return; }
    dataset.addBits(window.max_window_size_bit_length);
    output_file.pushInt(window_length, window.max_window_size_bit_length);
    codeValueRaw(window_value);
}

std::string CoderCA::getInfo() {
    return "a";
}
