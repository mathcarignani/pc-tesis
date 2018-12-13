
#ifndef CPP_PROJECT_LINEAR_CODER_UTILS_H
#define CPP_PROJECT_LINEAR_CODER_UTILS_H

#include "constants.h"
#include "decoder_cols.h"

class LinearCoderUtils {

public:
#if MASK_MODE
    static std::vector<int> createXCoordsVectorCA(DecoderBase* decoder, int window_size, int row_index, int nodata_sum);
    static std::vector<int> createXCoordsVectorPWLH(DecoderBase* decoder, int window_size, int row_index);
    static void addPointsWithNoData(Column* column, int window_size, std::vector<std::string> decoded_points,
                                    std::vector<int> x_coords_with_nodata);
#endif
};

#endif //CPP_PROJECT_LINEAR_CODER_UTILS_H
