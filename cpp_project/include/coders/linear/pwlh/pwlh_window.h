
#ifndef CPP_PROJECT_PWLH_WINDOW_H
#define CPP_PROJECT_PWLH_WINDOW_H

#include <string>
#include "LinearBucket.h"
#include "range.h"
#include <vector>
#include "constants.h"

class PWLHWindow {

private:
    int window_size;
    int error_threshold;
    LinearBucket* bucket;
    Range range;
    bool integer_mode;

public:
    int window_size_bit_length;
    int length;
    int x_coord;
    std::string constant_value;
    float constant_value_float;
    Point p1;
    Point p2;
#if !MASK_MODE
    bool nan_window;
#endif

    PWLHWindow(int window_size_, int error_threshold_, Range range_, bool integer_mode_);
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
