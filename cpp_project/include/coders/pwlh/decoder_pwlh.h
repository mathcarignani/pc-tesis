
#ifndef CPP_PROJECT_DECODER_PWLH_H
#define CPP_PROJECT_DECODER_PWLH_H

#include "decoder_cols.h"

class DecoderPWLH: public DecoderCols {

private:
    int max_window_size_bit_length;
    bool integer_mode;

    std::vector<std::string> decodeColumn() override;
    void decodeWindow(std::vector<std::string> & column);
    void decodeWindowDouble(std::vector<std::string> & column, int window_size);
    void decodeWindowInt(std::vector<std::string> & column, int window_size);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int max_window_size_, bool integer_mode_);
};

#endif //CPP_PROJECT_DECODER_PWLH_H
