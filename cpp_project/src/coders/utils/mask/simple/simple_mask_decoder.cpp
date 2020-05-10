#include "simple_mask_decoder.h"

#if MASK_MODE

#include "assert.h"

Mask* SimpleMaskDecoder::decode(DecoderCommon* decoder){
    Mask* mask = new Mask();
    int row_index = 0;
    Burst* burst = NULL;
    while (row_index < decoder->data_rows_count){
        bool no_data = decoder->decodeBool();
        int length = decoder->decodeInt(Constants::MASK_BITS) + 1; // 1 <= length <= Constants::MASK_MAX_SIZE
        burst = new Burst(no_data, length);
        mask->add(burst);
        row_index += burst->length;
    }
    assert(row_index == decoder->data_rows_count);
    mask->reset();
    return mask;
}

#endif // MASK_MODE
