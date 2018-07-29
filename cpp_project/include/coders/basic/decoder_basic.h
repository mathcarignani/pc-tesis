
#ifndef CPP_PROJECT_DECODER_BASIC_H
#define CPP_PROJECT_DECODER_BASIC_H

#include "decoder_cols.h"

class DecoderBasic: public DecoderCols {

private:
    std::vector<std::string> decodeDataColumn() override;

public:
    using DecoderCols::DecoderCols;
};

#endif //CPP_PROJECT_DECODER_BASIC_H
