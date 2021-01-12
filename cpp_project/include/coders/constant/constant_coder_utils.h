
#ifndef CPP_PROJECT_CONSTANT_CODER_UTILS_H
#define CPP_PROJECT_CONSTANT_CODER_UTILS_H

#include "conversor.h"
#include "math_utils.h"

class ConstantCoderUtils {

public:

    static std::string calculateConstantValue(double min, double max){
        int constant = min + max;
        if (constant != 0) { constant /= 2; }
        return Conversor::intToString(constant);
    }

    static bool validThreshold(int min, int max, double error_threshold){
        double width = MathUtils::intAbsolute(max - min);
        return width <= 2*error_threshold;
    }

};

#endif //CPP_PROJECT_CONSTANT_CODER_UTILS_H
