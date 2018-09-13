
#include "fr_window.h"
#include "string_utils.h"
#include "assert.h"
#include <iostream>
#include "ca_line.h"
#include "math_utils.h"
#include "vector_utils.h"

FRWindow::FRWindow(int max_window_size_, int error_threshold_){
    max_window_size = max_window_size_;
    error_threshold = error_threshold_;
    length = 0;
    data.reserve(max_window_size_);
}

void FRWindow::clear(){
    length = 0;
}

void FRWindow::addDataItem(int timestamp, std::string value){
    assert(length <= max_window_size);
//    std::cout << "value = " << value << std::endl;
    int new_timestamp = (length == 0) ? 0 : data[length-1].timestamp + timestamp;
    int value_int = StringUtils::stringToInt(value);
//    std::cout << "(length, value_int, new_timestamp) = (" << length << ", " << value_int << ", " << new_timestamp << ")" << std::endl;
    data[length] = DataItem(value_int, new_timestamp);
    length++;
}

bool FRWindow::isFull(){
    return length == max_window_size;
}

bool FRWindow::isEmpty(){
    return length == 0;
}

std::vector<DataItem> FRWindow::getItems(){
    std::vector<int> array{};
    getIndexes(array, 0, length - 1);
    VectorUtils::printIntVector(array);
    std::vector<DataItem> result;
    for(int i=0; i < array.size(); i++) { result.push_back(data[i]); }
    return result;
}

void FRWindow::getIndexes(std::vector<int> & array, int first_index, int last_index){
    if (!VectorUtils::vectorIncludesInt(array, first_index)) { array.push_back(first_index); }
    if ((first_index + 1 < last_index) && violatedConstraint(first_index, last_index)) {
        // displace segment
        int half = MathUtils::half(first_index, last_index);
        getIndexes(array, first_index, half);
        getIndexes(array, half, last_index);
    }
    if (!VectorUtils::vectorIncludesInt(array, last_index)) { array.push_back(last_index); }
}

bool FRWindow::violatedConstraint(int first_index, int last_index){
    DataItem first_item, last_item;
    first_item = data[first_index];
    last_item = data[last_index];

    CAPoint first_point, last_point;
    first_point = CAPoint(first_item);
    last_point = CAPoint(last_item);

    CALine line = CALine(first_point, last_point);
    for(int i=first_index+1; i < last_index; i++){
        CAPoint point = CAPoint(data[i]);
        double dis = line.distance(point);
        if (dis > error_threshold){
            return true;
        }
    }
    return false;
}