
#ifndef CPP_PROJECT_CODER_UTILS_H
#define CPP_PROJECT_CODER_UTILS_H

#include <vector>

class CoderUtils {

public:
    static std::vector<int> createXCoordsVector(std::vector<int> time_delta_vector, int window_size, int row_index);
};

#endif //CPP_PROJECT_CODER_UTILS_H
