
#include "math_utils.h"
#include <cmath>
#include <cstdlib>

//
// SOURCE: https://stackoverflow.com/a/21192373/4547232
//
// Examples:
// MathUtils::bitLength(0) == 1 // 0
// MathUtils::bitLength(1) == 1 // 1
// MathUtils::bitLength(2) == 2 // 10
// MathUtils::bitLength(3) == 2 // 11
// MathUtils::bitLength(4) == 3 // 100
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