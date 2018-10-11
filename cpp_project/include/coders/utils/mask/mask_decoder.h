
#ifndef CPP_PROJECT_MASK_DECODER_H
#define CPP_PROJECT_MASK_DECODER_H

#include "constants.h"

#if MASK_MODE

#include "decoder_base.h"
#include "mask.h"

class MaskDecoder {

public:
    static Mask* decode(DecoderBase* decoder, int data_rows_count);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_DECODER_H
