
#include "arithmetic_mask_decoder.h"

#if MASK_MODE == 3

#include "decompressor.h"
#include "decoder_input.h"
#include "decoder_output.h"
#include "modelKT.h"

ArithmeticMaskDecoder::ArithmeticMaskDecoder(DecoderBase* decoder_){
    decoder = decoder_;
    mask = new Mask();
}

Mask* ArithmeticMaskDecoder::decode(){
    flush();
    callDecompress();
    flush();
    mask->reset();
    return mask;
}

void ArithmeticMaskDecoder::flush(){
    // std::cout << "D1 >> decoder->flushByte();" << std::endl;
    decoder->flushByte();
    // std::cout << "D1 >> decoder->flushByte();" << std::endl;
}

void ArithmeticMaskDecoder::callDecompress(){
    DecoderInput input(decoder->input_file);
    DecoderOutput output(mask, decoder->data_rows_count);
    modelKT<int, 16, 14> model;

    decompress(input, output, model);

    output.close();
}

#endif // MASK_MODE == 3
