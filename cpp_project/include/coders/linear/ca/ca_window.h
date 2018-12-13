
#ifndef CPP_PROJECT_WINDOW_CA_H
#define CPP_PROJECT_WINDOW_CA_H

#include <string>
#include "Line.h"

class CAWindow {

private:
    int window_size;
    int error_threshold;
    Point* archived_value;
    Point* snapshot_value;
    Line* s_min;
    Line* s_max;

    Line* sMin(Point* point1, Point* point2, int error_threshold);
    Line* sMax(Point* point1, Point* point2, int error_threshold);

public:
    int window_size_bit_length;
    int length;
    std::string constant_value;
    int x_coord;
    bool nan_window;

    CAWindow(int window_size_, int error_threshold_);
    bool isFull();
    bool isEmpty();
    void createNonNanWindow(std::string incoming_value_str, int incoming_value);
    void createNanWindow();
    bool conditionHolds(int x_delta, int x_int, std::string x);
    void setWindow(int x_delta, int x_int, std::string x);
    void increaseLength();
    void printState();
};

#endif //CPP_PROJECT_WINDOW_CA_H
