
#include "pwlh_window.h"
#include "string_utils.h"
#include "math_utils.h"
#include "constants.h"


PWLHWindow::PWLHWindow(int window_size_, int error_threshold_, Range* range_, bool integer_mode_): Window(window_size_, error_threshold_){
    range = range_;
    bucket = new LinearBucket(error_threshold);
    length = 0; x_coord = 0;
    integer_mode = integer_mode_;
#if !MASK_MODE
    nan_window = false;
#endif
}

//
// PRE: x_delta >= 0
//
bool PWLHWindow::conditionHolds(std::string x, int x_delta){
    if (isEmpty()){ // this condition is only true the first time this method is called
        addFirstValue(x);
        return true;
    }
    else if (isFull()){
        return false;
    }
#if !MASK_MODE
    if (Constants::isNoData(x)){
        if (nan_window){ length++; return true;  }
        else {                     return false; }
    }
#endif
    // x is an integer
#if !MASK_MODE
    if (nan_window) { return false; }
#endif
    if (x_delta == 0) { return false; } // when x_delta == 0 we need to create a new window

    int x_int = StringUtils::stringToInt(x);
    int new_x_coord = x_coord + x_delta;
    bucket->addPointMOD(new_x_coord, x_int);

    if (bucket->checkEpsConstraint() && checkIntegerModeConstraint(new_x_coord)){ // bucket is valid
        length++; x_coord = new_x_coord;
        return true;
    }
    // bucket is invalid
    bucket->removePoint();
    bucket->getAproximatedLineMOD(p1, p2, x_coord);
#if CHECKS
    assert(p1.x == 0);
    assert(p2.x == x_coord);
#endif
    return false;
}

bool PWLHWindow::checkIntegerModeConstraint(int new_x_coord){
    bucket->getAproximatedLineMOD(p1, p2, new_x_coord);
    if (!integer_mode){ return true; }

    // this constraint is only checked when running in integer mode
    return range->insideRange(MathUtils::doubleToInt(p1.y)) && range->insideRange(MathUtils::doubleToInt(p2.y));
}

bool PWLHWindow::isFull(){
    return length == window_size;
}

bool PWLHWindow::isEmpty(){
    return length == 0;
}

void PWLHWindow::addFirstValue(std::string x){
    length = 1;
#if !MASK_MODE
    if (Constants::isNoData(x)){
        nan_window = true;
        constant_value = Constants::NO_DATA;
        constant_value_float = 0; // doesn't matter
        return;
    }
#endif
    // x is an integer
#if !MASK_MODE
    nan_window = false;
#endif
    x_coord = 0;
    int x_int = StringUtils::stringToInt(x);
    if (bucket->getSize() != 0) { bucket->resetBucket(); }
    bucket->addPointMOD(0, (double) x_int); // should be the same as calling bucket->addPoint((double) x_int);
    constant_value = x;
    constant_value_float = (float) x_int;
}

float PWLHWindow::getPoint1Y(){
    return p1.y;
}

float PWLHWindow::getPoint2Y(){
    return p2.y;
}

std::string PWLHWindow::getPoint1YIntegerMode(){
    return StringUtils::doubleToString(p1.y);
}

std::string PWLHWindow::getPoint2YIntegerMode(){
    return StringUtils::doubleToString(p2.y);
}
