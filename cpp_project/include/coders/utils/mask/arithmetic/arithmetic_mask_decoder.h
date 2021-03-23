
#ifndef CPP_PROJECT_ARITHMETIC_MASK_DECODER_H
#define CPP_PROJECT_ARITHMETIC_MASK_DECODER_H

#include "constants.h"

#if MASK_MODE

#include "mask.h"
#include "decoder_common.h"

class ArithmeticMaskDecoder {

private:
    DecoderCommon* decoder;
    int first_column_index = 0; // index of the first masked column
    int last_column_index = 0; // index of the last masked column
    Mask* mask;

    void flush();
    std::vector<Mask*> callDecompress();

public:
    ArithmeticMaskDecoder(DecoderCommon* decoder_, int first_column_index_, int last_column_index_);
    std::vector<Mask*> decode();

};

#endif // MASK_MODE

#endif //CPP_PROJECT_ARITHMETIC_MASK_DECODER_H
