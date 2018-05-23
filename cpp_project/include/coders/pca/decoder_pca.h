
#ifndef CPP_PROJECT_DECODER_PCA_H
#define CPP_PROJECT_DECODER_PCA_H

#include "decoder_cols.h"

class DecoderPCA: public DecoderCols {

private:
    std::vector<std::string> decodeColumn() override;

public:
    using DecoderCols::DecoderCols;
};

#endif //CPP_PROJECT_DECODER_PCA_H
