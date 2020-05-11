
#ifndef CPP_PROJECT_DECODER_BASE_H
#define CPP_PROJECT_DECODER_BASE_H

#include "decoder_cols.h"

class DecoderBase: public DecoderCols {

private:
    std::vector<std::string> decodeDataColumn() override;

public:
    using DecoderCols::DecoderCols;
};

#endif //CPP_PROJECT_DECODER_BASE_H
