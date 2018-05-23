
#ifndef CPP_PROJECT_PCA_WINDOW_H
#define CPP_PROJECT_PCA_WINDOW_H

#include <vector>
#include <string>

class PCAWindow {

private:
    int fixed_window_size;
    void updateMinAndMax(int x_int);
    void updateConstantValue();

public:
    int error_threshold;
    int length;
    bool nan_window;
    int min;
    int max;
    std::string constant_value;
    std::vector<std::string> *array;

    PCAWindow(int error_threshold_, int fixed_window_size_);
    void addValue(std::string x); // PRE: !isFull()
    bool isFull();
    bool isEmpty();
    bool hasConstantValue();
    void clearWindow();
    static bool validThreshold(int min, int max, int error_threshold);
    std::string getElement(int pos); // PRE: pos < length
};

#endif //CPP_PROJECT_PCA_WINDOW_H
