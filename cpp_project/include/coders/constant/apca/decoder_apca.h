
#ifndef CPP_PROJECT_DECODER_APCA_H
#define CPP_PROJECT_DECODER_APCA_H

#include "decoder_pca.h"

class DecoderAPCA: public DecoderPCA {

private:
    std::vector<std::string> decodeDataColumn() override;


public:
    using DecoderPCA::DecoderPCA;
    static std::vector<std::string> decodeDataColumn(DecoderCommon* decoder);
    static void decodeWindow(DecoderCommon* decoder, std::vector<std::string> & column);
};

#endif //CPP_PROJECT_DECODER_APCA_H
