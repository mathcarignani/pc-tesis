
#ifndef CPP_PROJECT_DECODER_PWLH_H
#define CPP_PROJECT_DECODER_PWLH_H

#include "decoder_cols.h"

class DecoderPWLH: public DecoderCols {

private:
    int max_window_size_bit_length;

    std::vector<std::string> decodeColumn() override;
    void decodeWindow(std::vector<std::string> & column);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int max_window_size_);
};

#endif //CPP_PROJECT_DECODER_PWLH_H
