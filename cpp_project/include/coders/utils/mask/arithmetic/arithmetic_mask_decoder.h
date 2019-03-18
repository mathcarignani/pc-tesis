
#ifndef CPP_PROJECT_ARITHMETIC_MASK_DECODER_H
#define CPP_PROJECT_ARITHMETIC_MASK_DECODER_H

#include "constants.h"

#if MASK_MODE == 3

#include "mask.h"
#include "decoder_base.h"

class ArithmeticMaskDecoder {

private:
    DecoderBase* decoder;
    Mask* mask;

    void flush();
    void callDecompress();

public:
    ArithmeticMaskDecoder(DecoderBase* decoder_);
    Mask* decode();

};

#endif // MASK_MODE == 3

#endif //CPP_PROJECT_ARITHMETIC_MASK_DECODER_H
