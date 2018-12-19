
#include "math_utils.h"
#include <cmath>
#include <cstdlib>

//
// SOURCE: https://stackoverflow.com/a/21192373/4547232
//
int MathUtils::bitLength(uint32_t value){
    int bits = 0;
    for (int bit_test = 16; bit_test > 0; bit_test >>= 1){
        if (value >> bit_test != 0){
            bits += bit_test;
            value >>= bit_test;
        }
    }
    return bits + 1;
}

int MathUtils::doubleToInt(double d){
    int d_int = (int)round(d);
    return d_int;
}

int MathUtils::intAbsolute(int value){
    return std::abs(value);
}

double MathUtils::doubleAbsolute(double value){
    return std::abs(value);
}

//
// PRE: first >= 0, last >= 0
//
int MathUtils::half(int first, int last){
    return (first + last) / 2;
}