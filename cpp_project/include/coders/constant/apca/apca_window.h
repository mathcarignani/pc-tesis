
#ifndef CPP_PROJECT_APCA_WINDOW_H
#define CPP_PROJECT_APCA_WINDOW_H

#include <string>
#include "constants.h"

class APCAWindow {

private:
    int window_size;
    int error_threshold;
    double min;
    double max;
#if !MASK_MODE
    bool nan_window;
#endif

public:
    int window_size_bit_length;
    int length;
    std::string constant_value;

    APCAWindow(int window_size_, int error_threshold_);
    bool conditionHolds(std::string x);
    bool isFull();
    bool isEmpty();
    void addFirstValue(std::string x);
    bool updateConstantValue(double new_min, double new_max);
};

#endif //CPP_PROJECT_APCA_WINDOW_H
