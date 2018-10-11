
#include "mask_decoder.h"

#if MASK_MODE

#include "assert.h"

void MaskDecoder::decode(DecoderBase* decoder, Mask* mask, int data_rows_count){
    int row_index = 0;
    while (row_index < data_rows_count){
        bool burst_is_no_data = decoder->decodeBool();
        int burst_length = decoder->decodeInt(Constants::MASK_BITS) + 1; // 1<= burst_length <= Constants::MASK_MAX_SIZE
        mask->add(burst_is_no_data, burst_length);
        row_index += burst_length;
    }
    assert(row_index == data_rows_count);
}

#endif

