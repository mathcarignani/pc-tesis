
#ifndef CPP_PROJECT_DECODER_CA_H
#define CPP_PROJECT_DECODER_CA_H

#include "decoder_cols.h"

class DecoderCA: public DecoderCols {

private:
    std::string archived_value;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow();
    void decodeValues(int window_size, std::string value);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int window_size_);
};

#endif //CPP_PROJECT_DECODER_CA_H
