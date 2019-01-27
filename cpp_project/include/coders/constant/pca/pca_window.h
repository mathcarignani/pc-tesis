
#ifndef CPP_PROJECT_PCA_WINDOW_H
#define CPP_PROJECT_PCA_WINDOW_H

#include <vector>
#include <string>
#include "constants.h"

class PCAWindow {

private:
    int window_size;
    int error_threshold;
    int min;
    int max;
#if !MASK_MODE
    bool nan_window;
#endif

    void updateMinAndMax(int x_int);
    void addNonFirstValue(std::string x); // PRE: !isFull() && !isEmpty()
    void addFirstValue(std::string x); // PRE: isEmpty()
    void updateConstantValue();

public:
    int length;
    bool has_constant_value;
    std::string constant_value;
    std::vector<std::string> *array;

    PCAWindow(int window_size_, int error_threshold_);
    void addValue(std::string x); // PRE: !isFull()
    bool isFull();
    bool isEmpty();
    void clearWindow();
    std::string getElement(int pos); // PRE: pos < length

};

#endif //CPP_PROJECT_PCA_WINDOW_H
