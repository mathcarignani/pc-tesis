
#ifndef CPP_PROJECT_CODER_UTILS_H
#define CPP_PROJECT_CODER_UTILS_H

#include <vector>
#include <string>
#include "constants.h"
#include "mask.h"
#include <iostream>

class CoderUtils {

public:
    static std::vector<int> createXCoordsVector(std::vector<int> time_delta_vector, int window_size, int row_index);
    static std::vector<int> createXCoordsVector(Mask* mask, std::vector<int> time_delta_vector, int window_size);
#if MASK_MODE
    static std::vector<int> createXCoordsVectorMaskMode(Mask* mask, std::vector<int> time_delta_vector, int init_delta_sum);
#endif
};

#endif //CPP_PROJECT_CODER_UTILS_H
