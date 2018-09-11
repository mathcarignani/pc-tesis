
#include "slide_filter_window.h"
#include "string_utils.h"

SlideFilterWindow::SlideFilterWindow() {}

SlideFilterWindow::SlideFilterWindow(int total_data_rows, int error_threshold_){
    data.reserve(total_data_rows);
    length = 0;
    error_threshold = error_threshold_;
}

void SlideFilterWindow::addDataItem(int timestamp, std::string value){
    int new_timestamp = (length == 0) ? 0 : data[length-1].timestamp + timestamp;
    int value_int = StringUtils::stringToInt(value);
    data[length] = DataItem(value_int, new_timestamp);
    length++;
}

int SlideFilterWindow::getDataLength() { return length; }

DataItem SlideFilterWindow::getAt(int pos) { return data[pos]; }

int SlideFilterWindow::getEsp() { return error_threshold; }
