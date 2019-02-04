
#ifndef CPP_PROJECT_WINDOW_H
#define CPP_PROJECT_WINDOW_H

#include "math_utils.h"

class Window {

protected:
    int window_size;
    int error_threshold;

public:
    int window_size_bit_length;
    int length;
    int constant_value;

    Window(){};

    Window(int window_size_, int error_threshold_){
        window_size = window_size_;
        error_threshold = error_threshold_;
        window_size_bit_length = MathUtils::bitLength(window_size);
    }
};

#endif //CPP_PROJECT_WINDOW_H
