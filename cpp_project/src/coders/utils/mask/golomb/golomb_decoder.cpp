
#include "golomb_decoder.h"
#include <math.h>

GolombDecoder::GolombDecoder(DecoderCommon* decoder_){
    decoder = decoder_;
}

void GolombDecoder::decode(Mask *mask){
    no_data_majority = decoder->decodeBool();
    k = decoder->decodeUnary();
    l = (int) pow(2, k);

    int row_index = 0;
    while (row_index < decoder->data_rows_count){
        row_index += decodeRunLength(mask, decoder->data_rows_count - row_index);
    }
    assert(row_index == decoder->data_rows_count);
}

int GolombDecoder::decodeRunLength(Mask* mask, int remaining){
    int length = decodeLength();

    if (length > 0){
        mask->add(no_data_majority, length);
        if (length == remaining) {
            return length;
        }
    }
    mask->add(!no_data_majority, 1);
    return length + 1;
}

int GolombDecoder::decodeLength(){
    if (k == 0){
        return decoder->decodeUnary();
    }
    // k > 0, l > 1
    int quot = decoder->decodeUnary();
    int rem = decoder->decodeInt(k);
    return l*quot + rem;
}
