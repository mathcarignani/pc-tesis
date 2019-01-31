
#include "apca_window.h"

#include "string_utils.h"
#include "math_utils.h"
#include "iostream"

APCAWindow::APCAWindow(int window_size_, int error_threshold_): Window(window_size_, error_threshold_){
    length = 0;
    min = 0;
    max = 0;
#if !MASK_MODE
    nan_window = false;
#endif
}

bool APCAWindow::conditionHolds(std::string x){
    if (isEmpty()){ // this condition is only true the first time this method is called
        addFirstValue(x);
        return true;
    }
    else if (isFull()){
        return false;
    }
#if !MASK_MODE
    if (Constants::isNoData(x)){
        if (nan_window){ length++; return true;  }
        else {                     return false; }
    }
    // x is an integer
    if (nan_window) { return false; }
#endif
    int x_int = StringUtils::stringToInt(x);
    if (x_int < min) { return updateConstantValue(x_int, max); }
    if (x_int > max) { return updateConstantValue(min, x_int); }
    // min <= x_int <= max
    length++;
    return true;
}

bool APCAWindow::updateConstantValue(int new_min, int new_max){
    if (!PCAWindow::validThreshold(new_min, new_max, error_threshold)) { return false; }

    // condition holds, update min, max and constant
    min = new_min; max = new_max;
    constant_value = PCAWindow::calculateConstantValue(min, max);
    length++;
    return true;
}

bool APCAWindow::isFull(){
    return length == window_size;
}

bool APCAWindow::isEmpty(){
    return length == 0;
}

void APCAWindow::addFirstValue(std::string x){
#if !MASK_MODE
    if (Constants::isNoData(x)){
        nan_window = true;
        constant_value = Constants::NO_DATA;
        length = 1;
        return;
    }
    // x is an integer
    nan_window = false;
#endif
    int x_int = StringUtils::stringToInt(x);
    min = x_int;
    max = x_int;
    constant_value = x;
    length = 1;
}