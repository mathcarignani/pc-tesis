
#ifndef CPP_PROJECT_DECODER_PCA_H
#define CPP_PROJECT_DECODER_PCA_H

#include "decoder_cols.h"

class DecoderPCA: public DecoderCols {

private:
    int fixed_window_size;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow(std::vector<std::string> & column, int window_size);
    void decodeConstantWindow(std::vector<std::string> & column, int window_size);
    void decodeNonConstantWindow(std::vector<std::string> & column, int window_size);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int fixed_window_size_);
};

#endif //CPP_PROJECT_DECODER_PCA_H
