
#ifndef CPP_PROJECT_DECODER_FR_H
#define CPP_PROJECT_DECODER_FR_H

#if MASK_MODE

#include "decoder_cols.h"
#include "DataItem.h"
#include "coder_utils.h"

class DecoderFR: public DecoderCols {

private:
    int max_window_size;
    int max_window_size_bit_length;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow(int window_size);
    std::vector<DataItem> readDataItems(int window_size);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int max_window_size_);
};

#endif //MASK_MODE

#endif //CPP_PROJECT_DECODER_FR_H
