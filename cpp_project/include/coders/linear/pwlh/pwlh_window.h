
#ifndef CPP_PROJECT_PWLH_WINDOW_H
#define CPP_PROJECT_PWLH_WINDOW_H

#include <string>
#include "LinearBucket.h"
#include "range.h"
#include <vector>
#include "constants.h"
#include "window.h"

class PWLHWindow: public Window {

private:
    LinearBucket* bucket;
    Range* range;
    bool integer_mode;

public:
    int x_coord;
    float constant_value_float;
    Point p1;
    Point p2;
#if !MASK_MODE
    bool nan_window;
#endif

    PWLHWindow(int window_size_, float error_threshold_, Range* range_, bool integer_mode_);
    bool conditionHolds(std::string x, int x_delta);
    bool checkIntegerModeConstraint(int new_x_coord);
    bool isFull();
    bool isEmpty();
    void addFirstValue(std::string x);
    float getPoint1Y();
    float getPoint2Y();
    std::string getPoint1YIntegerMode();
    std::string getPoint2YIntegerMode();
};

#endif //CPP_PROJECT_PWLH_WINDOW_H
