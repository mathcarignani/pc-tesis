
#include "pca_window.h"

#include <iostream>
#include <math_utils.h>
#include "string_utils.h"
#include "constant_coder_utils.h"

PCAWindow::PCAWindow(int window_size_, int error_threshold_): Window(window_size_, error_threshold_){
    array = new std::vector<std::string>;
    length = 0;
    has_constant_value = true;
    min = 0;
    max = 0;
#if !MASK_MODE
    nan_window = false;
#endif
}

void PCAWindow::updateMinAndMax(int x_int){
    if (x_int < min)      { min = x_int; }
    else if (x_int > max) { max = x_int; }
}

void PCAWindow::updateConstantValue(){
    constant_value = ConstantCoderUtils::calculateConstantValue(min, max);
}

void PCAWindow::addValue(std::string x){
    if (isEmpty()) { addFirstValue(x);    }
    else           { addNonFirstValue(x); }
    array->push_back(x);
    length++;
}

void PCAWindow::addFirstValue(std::string x){
#if !MASK_MODE
    if (Constants::isNoData(x)){
        nan_window = true;
        constant_value = Constants::NO_DATA;
        return;
    }
    // x is an integer
    nan_window = false;
#endif
    int x_int = StringUtils::stringToInt(x);
    min = x_int;
    max = x_int;
    constant_value = x;
}

void PCAWindow::addNonFirstValue(std::string x){
#if !MASK_MODE
    if (Constants::isNoData(x)){
        if (!nan_window){ has_constant_value = false; }
        return;
    }
    // x is an integer
    if (nan_window) { has_constant_value = false; }
#endif
    if (!has_constant_value) { return; }

    int x_int = StringUtils::stringToInt(x);
    updateMinAndMax(x_int);
    if (ConstantCoderUtils::validThreshold(min, max, error_threshold)){
        updateConstantValue();
    }
    else {
        has_constant_value = false;
    }
}

bool PCAWindow::isFull(){
    return length == window_size;
}

bool PCAWindow::isEmpty(){
    return length == 0;
}

void PCAWindow::clearWindow(){
    array->clear();
    length = 0;
    has_constant_value = true;
}

std::string PCAWindow::getElement(int pos){
    return array->at(pos);
}
