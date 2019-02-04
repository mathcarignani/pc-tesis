
#ifndef CPP_PROJECT_APCA_WINDOW_H
#define CPP_PROJECT_APCA_WINDOW_H

#include <string>
#include "pca_window.h"

class APCAWindow: public Window {

private:
    int min;
    int max;
#if !MASK_MODE
    bool nan_window;
#endif

public:
    APCAWindow(int window_size_, int error_threshold_);
    bool conditionHolds(int value);
    bool isFull();
    bool isEmpty();
    void addFirstValue(int value);
    bool updateConstantValue(int new_min, int new_max);
};

#endif //CPP_PROJECT_APCA_WINDOW_H
