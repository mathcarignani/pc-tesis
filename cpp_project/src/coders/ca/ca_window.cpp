
#include "ca_window.h"

#include "string_utils.h"
#include <iostream>

CAWindow::CAWindow() {}

CAWindow::CAWindow(int max_window_size_, int error_threshold_){
    max_window_size = max_window_size_;
    max_window_size_bit_length = StringUtils::bitLength(max_window_size);
    error_threshold = error_threshold_;
    createNanWindow();
    length = 0;
}

void CAWindow::updateSMinAndSMax(CAPoint incoming_point){
    CALine s_min_new = CALine::sMin(archived_value, incoming_point, error_threshold);
    CALine s_max_new = CALine::sMax(archived_value, incoming_point, error_threshold);

    if (s_min_new.yIntersection(incoming_point) > s_min.yIntersection(incoming_point)){
        s_min = s_min_new;
    }

    if (s_max_new.yIntersection(incoming_point) < s_max.yIntersection(incoming_point)){
        s_max = s_max_new;
    }
}

void CAWindow::createNonNanWindow(std::string incoming_value_str, int incoming_value){
    nan_window = false;
    constant_value = incoming_value_str;
    archived_value = CAPoint(0, incoming_value);
    snapshot_value = archived_value;
    length = 0;
    s_min = CALine();
    s_max = CALine();
}

void CAWindow::createNanWindow(){
    nan_window = true;
    constant_value = "N";
    archived_value = CAPoint(); // we don't use this value
    snapshot_value = archived_value; // we don't use this value
    length = 1;
    s_min = CALine(); // we don't use this value
    s_max = CALine(); // we don't use this value
}

bool CAWindow::conditionHolds(CAPoint incoming_point, std::string x){
    bool condition_holds = not (s_min.pointBelowLine(incoming_point) or s_max.pointAboveLine(incoming_point));
    if (condition_holds){
        snapshot_value = incoming_point;
        constant_value = x;
        updateSMinAndSMax(incoming_point);
        length++;
    }
    return condition_holds;
}

void CAWindow::updateValues(std::string x, int x_int){
    length = 1;
    snapshot_value = CAPoint(length, x_int);
    constant_value = x;
    s_min = CALine::sMin(archived_value, snapshot_value, error_threshold);
    s_max = CALine::sMax(archived_value, snapshot_value, error_threshold);
}

void CAWindow::updateLength(int new_length){
    length = new_length;
}

bool CAWindow::isFull(){
    return length == max_window_size;
}

bool CAWindow::isEmpty(){
    return length == 0;
}

void CAWindow::printState(){
    std::cout << "archived_value = "; archived_value.print();
    std::cout << "constant_value = " << constant_value << std::endl;
    std::cout << "snapshot_value = "; snapshot_value.print(); std::cout << std::endl;
    std::cout << "s_min = "; s_min.print(); std::cout << std::endl;
    std::cout << "s_max = "; s_max.print(); std::cout << std::endl;
}
