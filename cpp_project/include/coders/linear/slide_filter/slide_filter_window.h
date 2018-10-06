
#ifndef CPP_PROJECT_SLIDE_FILTER_WINDOW_H
#define CPP_PROJECT_SLIDE_FILTER_WINDOW_H

#include <string>
#include <vector>
#include "Line.h"

class CoderSlideFilter;

class SlideFilterWindow {

private:
    std::vector<DataItem> data;
    int error_threshold;
    int total_data_rows;
    CoderSlideFilter* coder;

public:
    int length;
    SlideFilterWindow(int total_data_rows_, int error_threshold_);
    SlideFilterWindow(CoderSlideFilter* coder_);
    CoderSlideFilter* getCompressData();
    void addDataItem(int timestamp, std::string value);
    int getDataLength();
    DataItem getAt(int pos);
    int getEsp();

};

#endif //CPP_PROJECT_SLIDE_FILTER_WINDOW_H
