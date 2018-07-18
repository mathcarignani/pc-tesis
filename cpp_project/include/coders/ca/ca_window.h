
#ifndef CPP_PROJECT_WINDOW_CA_H
#define CPP_PROJECT_WINDOW_CA_H

#include <string>
#include "ca_point.h"
#include "ca_line.h"

class CAWindow {

private:
    int max_window_size;
    int error_threshold;
    CAPoint archived_value;
    CAPoint snapshot_value;
    CALine s_min;
    CALine s_max;

public:
    int max_window_size_bit_length;
    int length;
    std::string constant_value;
    bool nan_window;

    CAWindow();
    CAWindow(int max_window_size_, int error_threshold_);
    bool isFull();
    bool isEmpty();
    void updateSMinAndSMax(CAPoint incoming_point);
    void createNonNanWindow(std::string incoming_value_str, int incoming_value);
    void createNanWindow();
    bool conditionHolds(CAPoint incoming_point, std::string x);
    void updateValues(std::string x, int x_int);
    void updateLength(int new_length);
    void printState();
};

#endif //CPP_PROJECT_WINDOW_CA_H