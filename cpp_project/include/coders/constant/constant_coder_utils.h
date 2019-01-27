
#ifndef CPP_PROJECT_CONSTANT_CODER_UTILS_H
#define CPP_PROJECT_CONSTANT_CODER_UTILS_H

#include "string_utils.h"
#include "math_utils.h"

class ConstantCoderUtils {

public:

    static std::string calculateConstantValue(int min, int max){
        int constant = min + max;
        if (constant != 0) { constant /= 2; }
        return StringUtils::intToString(constant);
    }

    static bool validThreshold(double min, double max, int error_threshold){
        double width = MathUtils::doubleAbsolute(max - min);
        return width <= 2*error_threshold;
    }

};

#endif //CPP_PROJECT_CONSTANT_CODER_UTILS_H
