
#include "coder_slide_filter.h"

void CoderSlideFilter::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderSlideFilter::codeColumnBefore(){
    window = createWindow();
}

void CoderSlideFilter::codeColumnWhile(std::string csv_value){
    // TODO
    // code(window, false, csv_value);
}

void CoderSlideFilter::codeColumnAfter(){
    // TODO
    // code(window, true, "0"); // force code
}

SlideFilterWindow CoderSlideFilter::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    return SlideFilterWindow(max_window_size, error_threshold);
}

//void CoderCA::code(CAWindow & window, bool force_code, std::string x){
//    if (force_code){
//        codeWindow(window, window.length, window.constant_value);
//    }
//    else if (window.isEmpty()){
//        if (x[0] == 'N'){ // this condition can only be true on the first iteration
//            window.createNanWindow();
//        }
//        else { // x is an integer
//            int x_int = std::stoi(x);
//            if (window.nan_window){
//                codeWindow(window, 1, x);
//                window.createNonNanWindow(x, x_int);
//            }
//            else {
//                window.updateValues(x, x_int);
//            }
//        }
//    }
//    else if (window.isFull()){
//        codeWindow(window, window.length, window.constant_value);
//        if (x[0] == 'N'){
//            window.createNanWindow();
//        }
//        else { // x is an integer
//            int x_int = std::stoi(x);
//            codeWindow(window, 1, x);
//            window.createNonNanWindow(x, x_int);
//        }
//    }
//    else if (x[0] == 'N'){
//        if (window.nan_window){
//            window.updateLength(window.length + 1);
//        }
//        else {
//            codeWindow(window, window.length, window.constant_value);
//            window.createNanWindow();
//        }
//    }
//    else { // x is an integer
//        int x_int = std::stoi(x);
//        if (window.nan_window){
//            codeWindow(window, window.length, window.constant_value); // code nan window
//            codeWindow(window, 1, x); // code single value window
//            window.createNonNanWindow(x, x_int);
//        }
//        else {
//            CAPoint incoming_point = CAPoint(window.length + 1, x_int);
//            if (not window.conditionHolds(incoming_point, x)){
////                std::cout << "(5.2)" << std::endl;
//                codeWindow(window, window.length, window.constant_value);
//                codeWindow(window, 1, x);
//                window.createNonNanWindow(x, x_int);
//            }
//            else {
////                std::cout << "(5.3)" << std::endl;
//            }
//        }
//    }
//}

void CoderSlideFilter::codeWindow(SlideFilterWindow & window, int window_length, std::string window_value){
    if (window_length == 0) { return; }
    codeInt(window_length, window.max_window_size_bit_length);
    codeValueRaw(window_value);
}
