
#ifndef CPP_PROJECT_SLIDE_FILTER_WINDOW_H
#define CPP_PROJECT_SLIDE_FILTER_WINDOW_H

#include <string>
#include <vector>
#include "Line.h"
#include "window.h"

class CoderSlideFilter;

class SlideFilterWindow: public Window {

private:
    std::vector<DataItem> data;
    int total_data_rows;
    CoderSlideFilter* coder;

public:
    SlideFilterWindow(int total_data_rows_, int error_threshold_);
    SlideFilterWindow(CoderSlideFilter* coder_);
    CoderSlideFilter* getCompressData();
    void addDataItem(int timestamp, std::string value);
    int getDataLength();
    DataItem getAt(int pos);
    int getEsp();
};

#endif //CPP_PROJECT_SLIDE_FILTER_WINDOW_H
