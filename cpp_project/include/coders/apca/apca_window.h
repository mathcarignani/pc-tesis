
#ifndef CPP_PROJECT_APCA_WINDOW_H
#define CPP_PROJECT_APCA_WINDOW_H

#include <string>

class APCAWindow {

private:
    int max_window_size;
    int error_threshold;
    bool nan_window;
    int min;
    int max;

public:
    int max_window_size_bit_length;
    int length;
    std::string constant_value;

    APCAWindow();
    APCAWindow(int max_window_size_, int error_threshold_);
    bool conditionHolds(std::string x);
    bool isFull();
    bool isEmpty();
    void addFirstValue(std::string x);
    bool updateConstantValue(int new_min, int new_max);
};

#endif //CPP_PROJECT_APCA_WINDOW_H
