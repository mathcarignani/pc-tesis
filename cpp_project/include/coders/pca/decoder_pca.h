
#ifndef CPP_PROJECT_DECODER_PCA_H
#define CPP_PROJECT_DECODER_PCA_H

#include "decoder_cols.h"

class DecoderPCA: public DecoderCols {

private:
    int fixed_window_size;

    std::vector<std::string> decodeDataColumn() override;

    /// !MASK_MODE
    std::vector<std::string> decodeDataColumnNoMask();
    void decodeWindow(std::vector<std::string> & column, int window_size);
    void decodeConstantWindow(std::vector<std::string> & column, int window_size);
    void decodeNonConstantWindow(std::vector<std::string> & column, int window_size);

    /// MASK_MODE
    std::vector<std::string> decodeDataColumnMaskMode();
    void decodeWindowMaskMode(std::vector<std::string> & column, int window_size);
    void decodeConstantWindowMaskMode(std::vector<std::string> & column, int window_size);
    void decodeNonConstantWindowMaskMode(std::vector<std::string> & column, int window_size);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int fixed_window_size_);
};

#endif //CPP_PROJECT_DECODER_PCA_H
