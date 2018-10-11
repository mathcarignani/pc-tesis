
#include "mask_decoder.h"

#if MASK_MODE

#include "assert.h"

void MaskDecoder::decode(DecoderBase* decoder, Mask* mask, int data_rows_count){
    int row_index = 0;
    Burst* burst = NULL;
    while (row_index < data_rows_count){
        bool no_data = decoder->decodeBool();
        int length = decoder->decodeInt(Constants::MASK_BITS) + 1; // 1<= burst_length <= Constants::MASK_MAX_SIZE
        burst = new Burst(no_data, length);
        mask->add(burst);
        row_index += burst->length;
    }
    assert(row_index == data_rows_count);
}

#endif

