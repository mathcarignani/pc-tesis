
#include "coder_utils.h"
#include <iostream>

std::vector<int> CoderUtils::createXCoordsVector(std::vector<int> time_delta_vector, int window_size, int row_index){
    std::vector<int> result;
    int current_sum = 0;
    int time_delta;
    for(int i = 0; i < window_size; i++){
        time_delta = (i == 0) ? 0 : time_delta_vector.at(row_index + i);
        current_sum += time_delta;
        result.push_back(current_sum);
    }
    return result;
}

std::vector<int> CoderUtils::createXCoordsVector(Mask* mask, std::vector<int> time_delta_vector, int window_size){
    mask->reset();
    std::vector<int> result;
    int current_sum = 0;
    int time_delta;
    int i = 0;
    int row_index = -1;
    while(i < window_size) {
        row_index++;
        if (mask->isNoData()) { continue; } // ignore these values
        time_delta = (i == 0) ? 0 : time_delta_vector.at(row_index);
        current_sum += time_delta;
        result.push_back(current_sum);
        i++;
    }
    return result;
}

#if MASK_MODE
//
// Returns a vector with the time deltas between no "nodata" values.
// If there are "nodata" values in the middle, their time delta is still considered.
//
std::vector<int> CoderUtils::createXCoordsVectorMaskMode(Mask* mask, std::vector<int> time_delta_vector, int init_delta_sum){
    mask->reset();
    std::vector<int> result;
    int delta_sum = init_delta_sum;
    for(int i=0; i < mask->total_data + mask->total_no_data; i++){
        delta_sum += time_delta_vector.at(i);
        if (mask->isNoData()) { continue; } // ignore these values
        result.push_back(delta_sum);
    }
    return result;
}
#endif // MASK_MODE