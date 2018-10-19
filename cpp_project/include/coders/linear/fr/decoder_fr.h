
#ifndef CPP_PROJECT_DECODER_FR_H
#define CPP_PROJECT_DECODER_FR_H

#include "decoder_cols.h"

#if MASK_MODE

#include "DataItem.h"

class DecoderFR: public DecoderCols {

private:
    int window_size;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow(int window_size, std::vector<int> x_coords);
    std::vector<DataItem> readDataItems(int window_size);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int window_size_);
};

#endif //MASK_MODE

#endif //CPP_PROJECT_DECODER_FR_H
