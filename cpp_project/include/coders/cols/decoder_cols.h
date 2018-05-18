
#ifndef CPP_PROJECT_DECODER_COLS_H
#define CPP_PROJECT_DECODER_COLS_H

#include "decoder_base.h"

class DecoderCols: public DecoderBase {

private:
    void decodeDataRows() override;
    virtual void decodeColumn() = 0;

public:
    using DecoderBase::DecoderBase;

};

#endif //CPP_PROJECT_DECODER_COLS_H
