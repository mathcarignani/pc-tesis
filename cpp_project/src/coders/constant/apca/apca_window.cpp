
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

bool APCAWindow::conditionHolds(int value){
    if (isEmpty()){ // this condition is only true the first time this method is called
        addFirstValue(value);
        return true;
    }
    else if (isFull()){
        return false;
    }
#if !MASK_MODE
    if (Constants::isNoData(value)){
        if (nan_window){ length++; return true;  }
        else {                     return false; }
    }
    // value is an integer
    if (nan_window) { return false; }
#endif
    if (value < min) { return updateConstantValue(value, max); }
    if (value > max) { return updateConstantValue(min, value); }
    // min <= value <= max
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

void APCAWindow::addFirstValue(int value){
    constant_value = value;
    length = 1;
#if !MASK_MODE
    if (Constants::isNoData(value)){
        nan_window = true;
        return;
    }
    // value is an integer
    nan_window = false;
#endif
    min = value;
    max = value;
}