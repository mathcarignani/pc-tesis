
#include "arithmetic_mask_decoder.h"

#if MASK_MODE

#include "decompressor.h"
#include "decoder_input.h"
#include "decoder_output.h"
#include "modelKT.h"

ArithmeticMaskDecoder::ArithmeticMaskDecoder(DecoderCommon* decoder_, int first_column_index_, int last_column_index_){
    decoder = decoder_;
    first_column_index = first_column_index_;
    last_column_index = last_column_index_;
}

std::vector<Mask*> ArithmeticMaskDecoder::decode(){
    flush();
    std::vector<Mask*> masks_vector = callDecompress();
    flush();
    return masks_vector;
}

void ArithmeticMaskDecoder::flush(){
    decoder->flushByte();
}

std::vector<Mask*> ArithmeticMaskDecoder::callDecompress(){
    DecoderInput input(decoder->input_file);
    DecoderOutput output(decoder->data_rows_count, first_column_index, last_column_index);
    modelKT<int, 16, 14> model;
    decompress(input, output, model);
    return output.masks_vector;
}

#endif // MASK_MODE
