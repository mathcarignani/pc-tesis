
#ifndef CPP_PROJECT_DECODER_PWLH_H
#define CPP_PROJECT_DECODER_PWLH_H

#include "decoder_cols.h"

class DecoderPWLH: public DecoderCols {

private:
    bool integer_mode;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow();
    void decodeWindowDouble(int window_size);
    void decodeWindowInt(int window_size);

#if !MASK_MODE
    void addPoints(int window_size, std::vector<std::string> decoded_points);
    void addNoDataPoints(int window_size);
#else
    std::vector<int> createXCoordsWithNoDataVector(int window_size);
    void addPointsWithNoData(int window_size, std::vector<std::string> decoded_points, std::vector<int> x_coords_with_nodata);
#endif

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int window_size_, bool integer_mode_);
};

#endif //CPP_PROJECT_DECODER_PWLH_H
