
#ifndef CPP_PROJECT_APCA_WINDOW_H
#define CPP_PROJECT_APCA_WINDOW_H

#include <string>
#include "constants.h"
#include "pca_window.h"

class APCAWindow: public Window {

private:
    double min;
    double max;
#if !MASK_MODE
    bool nan_window;
#endif

public:
    APCAWindow(int window_size_, int error_threshold_);
    bool conditionHolds(std::string x);
    bool isFull();
    bool isEmpty();
    void addFirstValue(std::string x);
    bool updateConstantValue(double new_min, double new_max);
};

#endif //CPP_PROJECT_APCA_WINDOW_H
