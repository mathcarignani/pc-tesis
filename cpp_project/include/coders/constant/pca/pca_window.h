
#ifndef CPP_PROJECT_PCA_WINDOW_H
#define CPP_PROJECT_PCA_WINDOW_H

#include <vector>
#include <string>
#include "constants.h"
#include "window.h"

class PCAWindow: public Window {

private:
    int min;
    int max;
#if !MASK_MODE
    bool nan_window;
#endif

    void updateMinAndMax(int value);
    void addNonFirstValue(int value); // PRE: !isFull() && !isEmpty()
    void addFirstValue(int value); // PRE: isEmpty()
    void updateConstantValue();

public:
    bool has_constant_value;
    std::vector<int> *array;

    PCAWindow(int window_size_, int error_threshold_);
    void addValue(int value); // PRE: !isFull()
    bool isFull();
    bool isEmpty();
    void clearWindow();
    int getElement(int pos); // PRE: pos < length

    static int calculateConstantValue(int min, int max);
    static bool validThreshold(int min, int max, int error_threshold);
};

#endif //CPP_PROJECT_PCA_WINDOW_H
