
#ifndef CPP_PROJECT_DECODER_CA_H
#define CPP_PROJECT_DECODER_CA_H

#include "decoder_cols.h"

class DecoderCA: public DecoderCols {

private:
    int max_window_size_bit_length;
    int current_window_size;
    std::string current_value;

    std::vector<std::string> decodeColumn() override;
    void decodeWindow(std::vector<std::string> & column);
    void createWindow(std::vector<std::string> & column, std::string previous_value);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int max_window_size_);
};

#endif //CPP_PROJECT_DECODER_CA_H
