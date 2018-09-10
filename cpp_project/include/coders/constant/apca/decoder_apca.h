
#ifndef CPP_PROJECT_DECODER_APCA_H
#define CPP_PROJECT_DECODER_APCA_H

#include "decoder_pca.h"

class DecoderAPCA: public DecoderPCA {

private:
    int max_window_size_bit_length;

    std::vector<std::string> decodeDataColumn() override;
    void decodeWindow(std::vector<std::string> & column);

public:
    using DecoderPCA::DecoderPCA;
    void setCoderParams(int max_window_size_);
};

#endif //CPP_PROJECT_DECODER_APCA_H
