
#ifndef CPP_PROJECT_WINDOW_CA_H
#define CPP_PROJECT_WINDOW_CA_H

#include <string>
#include "Line.h"
#include "window.h"

class CAWindow: public Window {

private:
    Point* archived_value;
    Point* snapshot_value;
    Line* s_min;
    Line* s_max;

    Line* sMin(Point* point1, Point* point2, int error_threshold);
    Line* sMax(Point* point1, Point* point2, int error_threshold);

public:
    int x_coord;
    bool nan_window;

    CAWindow(int window_size_, int error_threshold_);
    bool isFull();
    bool isEmpty();
    void createNonNanWindow(int incoming_value);
    void createNanWindow();
    bool conditionHolds(int value_delta, int value);
    void setWindow(int value_delta, int value);
    void increaseLength();
    void printState();
};

#endif //CPP_PROJECT_WINDOW_CA_H
