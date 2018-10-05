
#include "slide_filter_window.h"
#include "string_utils.h"
#include "iostream"
#include "assert.h"

SlideFilterWindow::SlideFilterWindow() {}

SlideFilterWindow::SlideFilterWindow(int total_data_rows_, int error_threshold_){
    total_data_rows = total_data_rows_;
    data.reserve(total_data_rows);
    length = 0;
    error_threshold = error_threshold_;
}

void SlideFilterWindow::addDataItem(int timestamp, std::string value){
    int new_timestamp = (length == 0) ? 0 : data[length-1].timestamp + timestamp;
    int value_int = StringUtils::stringToInt(value);
    data[length] = DataItem(value_int, new_timestamp);
//    std::cout << "(length, value_int, new_timestamp) = (" << length << ", " << value_int << ", " << new_timestamp << ")" << std::endl;
    length++;
}

int SlideFilterWindow::getDataLength() { return length; }

DataItem SlideFilterWindow::getAt(int pos) { return data[pos]; }

int SlideFilterWindow::getEsp() { return error_threshold; }

//int SlideFilterWindow::getPosition(int timestamp) {
//    std::cout << "getPosition(" << timestamp << ")" << std::endl;
//    int index = 0;
//    int index_timestamp;
//    while (index < total_data_rows) {
//        index_timestamp = data[index].timestamp;
//        if (index_timestamp == timestamp) { return index; }
//        if (index_timestamp > timestamp) { assert(1 == 0); } // error
//        index++;
//    }
//}