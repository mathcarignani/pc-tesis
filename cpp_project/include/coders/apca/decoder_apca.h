
#ifndef CPP_PROJECT_DECODER_APCA_H
#define CPP_PROJECT_DECODER_APCA_H

#include "decoder_cols.h"

class DecoderAPCA: public DecoderCols {

private:
    int max_window_size_bit_length;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow(std::vector<std::string> & column);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int max_window_size_);
};

#endif //CPP_PROJECT_DECODER_APCA_H
