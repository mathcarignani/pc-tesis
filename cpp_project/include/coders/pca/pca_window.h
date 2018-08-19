
#ifndef CPP_PROJECT_PCA_WINDOW_H
#define CPP_PROJECT_PCA_WINDOW_H

#include <vector>
#include <string>
#include "constants.h"

class PCAWindow {

private:
    int fixed_window_size;
    int error_threshold;
    int min;
    int max;
#if MASK_MODE
    bool nan_window;
#endif

    void updateMinAndMax(int x_int);
    void updateConstantValue();
    void addFirstValue(std::string x); // PRE: isEmpty()
    void addNonFirstValue(std::string x); // PRE: !isFull() && !isEmpty()

public:
    int length;
    bool has_constant_value;
    std::string constant_value;
    std::vector<std::string> *array;

    PCAWindow();
    PCAWindow(int fixed_window_size_, int error_threshold_);
    void addValue(std::string x); // PRE: !isFull()
    bool isFull();
    bool isEmpty();
    void clearWindow();
    std::string getElement(int pos); // PRE: pos < length

    static bool validThreshold(int min, int max, int error_threshold);
};

#endif //CPP_PROJECT_PCA_WINDOW_H
