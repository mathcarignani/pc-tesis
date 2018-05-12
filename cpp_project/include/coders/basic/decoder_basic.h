
#ifndef CPP_PROJECT_DECODER_BASIC_H
#define CPP_PROJECT_DECODER_BASIC_H

#include "decoder_base.h"

class DecoderBasic: public DecoderBase {

private:
    void decodeDataRows() override;

public:
    using DecoderBase::DecoderBase;
};

#endif //CPP_PROJECT_DECODER_BASIC_H
