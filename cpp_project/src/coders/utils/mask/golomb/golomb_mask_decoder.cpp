
#include "golomb_mask_decoder.h"

#if MASK_MODE

#include "assert.h"
#include "golomb_decoder.h"

Mask* GolombMaskDecoder::decode(DecoderBase* decoder){
    Mask* mask = new Mask();

    bool single_burst = decoder->decodeBool();
    if (single_burst){ // p in {0, 1}
        bool no_data_burst = decoder->decodeBool();
        Burst* burst = new Burst(no_data_burst, decoder->data_rows_count);
        mask->add(burst);
    }
    else { // 0 < p < 1
        GolombDecoder* golomb_decoder = new GolombDecoder(decoder);
        golomb_decoder->decode(mask);
    }
    mask->reset();
    return mask;
}

#endif // MASK_MODE
