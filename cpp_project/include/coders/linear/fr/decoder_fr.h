
#ifndef CPP_PROJECT_DECODER_FR_H
#define CPP_PROJECT_DECODER_FR_H

#include "decoder_cols.h"

class DecoderFR: public DecoderCols {

private:
    int max_window_size;
    int max_window_size_bit_length;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow(std::vector<std::string> & column, int window_size);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int max_window_size_);
};

#endif //CPP_PROJECT_DECODER_FR_H
