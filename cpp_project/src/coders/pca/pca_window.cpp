
#include "pca_window.h"

#include <iostream>

PCAWindow::PCAWindow() {}

PCAWindow::PCAWindow(int fixed_window_size_, int error_threshold_){
    fixed_window_size = fixed_window_size_;
    error_threshold = error_threshold_;
    array = new std::vector<std::string>;
    length = 0;
    nan_window = false;
    min = 0;
    max = 0;
}

void PCAWindow::updateMinAndMax(int x_int){
    if (x_int < min) { min = x_int; }
    else if (x_int > max) { max = x_int; }
}

void PCAWindow::updateConstantValue(){
    int constant = min + max;
    if (constant != 0) { constant /= 2; }
    constant_value = std::to_string(constant);
}

void PCAWindow::addValue(std::string x){
    if (isEmpty()){ addFirstValue(x);    }
    else {         addNonFirstValue(x); }
    array->push_back(x);
    length++;
}

void PCAWindow::addFirstValue(std::string x){
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

void PCAWindow::addNonFirstValue(std::string x){
    if (x[0] == 'N'){ // TODO: move 'N' to a constant
        if (!nan_window){
            constant_value = "";
        }
    }
    else { // x is an integer
        if (nan_window) {
            nan_window = false;
            constant_value = "";
        }
        else if (hasConstantValue()){
            int x_int = std::stoi(x);
            updateMinAndMax(x_int);
            bool valid_threshold = validThreshold(min, max, error_threshold);
            if (valid_threshold){
                updateConstantValue();
            }
            else {
                constant_value = "";
            }
        }
    }
}

bool PCAWindow::isFull(){
    return length == fixed_window_size;
}

bool PCAWindow::isEmpty(){
    return length == 0;
}

bool PCAWindow::hasConstantValue(){
    return !constant_value.empty();
}

void PCAWindow::clearWindow(){
    array->clear();
    length = 0;
}

bool PCAWindow::validThreshold(int min, int max, int error_threshold){
    int min_val_aux = min + std::abs(min); // >= 0
    int max_val_aux = max + std::abs(min); // >= 0
    int width = max_val_aux - min_val_aux; // >= 0
    return width <= 2*error_threshold;
}

std::string PCAWindow::getElement(int pos){
    return array->at(pos);
}
