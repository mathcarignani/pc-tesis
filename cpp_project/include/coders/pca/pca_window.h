
#ifndef CPP_PROJECT_PCA_WINDOW_H
#define CPP_PROJECT_PCA_WINDOW_H

#include <vector>
#include <string>

class PCAWindow {

private:
    int fixed_window_size;
    int error_threshold;
    bool nan_window;
    int min;
    int max;

    void updateMinAndMax(int x_int);
    void updateConstantValue();
    void addFirstValue(std::string x); // PRE: isEmpty()
    void addNonFirstValue(std::string x); // PRE: !isFull() && !isEmpty()

public:
    int length;
    std::string constant_value;
    std::vector<std::string> *array;

    PCAWindow(int fixed_window_size_, int error_threshold_);
    void addValue(std::string x); // PRE: !isFull()
    bool isFull();
    bool isEmpty();
    bool hasConstantValue();
    void clearWindow();
    static bool validThreshold(int min, int max, int error_threshold);
    std::string getElement(int pos); // PRE: pos < length
};

#endif //CPP_PROJECT_PCA_WINDOW_H
