
#include "apca_window.h"

#include "string_utils.h"
#include "pca_window.h"

APCAWindow::APCAWindow() {}

APCAWindow::APCAWindow(int max_window_size_, int error_threshold_){
    max_window_size = max_window_size_;
    max_window_size_bit_length = StringUtils::bitLength(max_window_size);
    error_threshold = error_threshold_;
    length = 0;
    nan_window = false;
    min = 0;
    max = 0;
}

bool APCAWindow::conditionHolds(std::string x){
    if (isEmpty()){ // this condition is only true the first time this method is called
        addFirstValue(x);
        return true;
    }
    else if (isFull()){
        return false;
    }
    else if (x[0] == 'N'){ // TODO: move 'N' to a constant
        if (nan_window){ length++; return true;  }
        else {                     return false; }
    }
    else { // x is an integer
        if (nan_window) { return false; }
        else {
            int x_int = std::stoi(x);
            if (x_int < min){
                return updateConstantValue(x_int, max);
            }
            else if (x_int > max){
                return updateConstantValue(min, x_int);
            }
            else { // min <= x_int && x_int <= max
                length++; return true;
            }
        }
    }
}

bool APCAWindow::updateConstantValue(int new_min, int new_max){
    if (!PCAWindow::validThreshold(new_min, new_max, error_threshold)) { return false; }
    else {
        // condition holds, update min, max and constant
        min = new_min;
        max = new_max;
        int constant = min + max;
        if (constant != 0) { constant /= 2; }
        constant_value = std::to_string(constant);
        length++; return true;
    }
}

bool APCAWindow::isFull(){
    return length == max_window_size;
}

bool APCAWindow::isEmpty(){
    return length == 0;
}

void APCAWindow::addFirstValue(std::string x){
    length = 1;
    if (x[0] == 'N'){ // TODO: move 'N' to a constant
        nan_window = true;
        constant_value = "N"; // TODO: move "N" to a constant
    }
    else { // x is an integer
        nan_window = false;
        int x_int = std::stoi(x);
        min = x_int;
        max = x_int;
        constant_value = x;
    }
}