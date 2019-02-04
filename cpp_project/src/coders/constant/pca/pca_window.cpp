
#include "pca_window.h"

#include <iostream>
#include <math_utils.h>
#include "string_utils.h"

PCAWindow::PCAWindow(int window_size_, int error_threshold_): Window(window_size_, error_threshold_){
    array = new std::vector<int>;
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
    constant_value = calculateConstantValue(min, max);
}

void PCAWindow::addValue(int value){
    if (isEmpty()) { addFirstValue(value);    }
    else           { addNonFirstValue(value); }
    array->push_back(value);
    length++;
}

void PCAWindow::addFirstValue(int value){
    constant_value = value;
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

void PCAWindow::addNonFirstValue(int value){
#if !MASK_MODE
    if (Constants::isNoData(value)){
        if (!nan_window){ has_constant_value = false; }
        return;
    }
    // value is an integer
    if (nan_window) { has_constant_value = false; }
#endif
    if (!has_constant_value) { return; }

    updateMinAndMax(value);
    if (validThreshold(min, max, error_threshold)){
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

int PCAWindow::getElement(int pos){
    return array->at(pos);
}

int PCAWindow::calculateConstantValue(int min, int max){
    int constant = min + max;
    if (constant != 0) { constant /= 2; }
    return constant;
}

bool PCAWindow::validThreshold(int min, int max, int error_threshold){
    int width = MathUtils::intAbsolute(max - min);
    return width <= 2*error_threshold;
}
