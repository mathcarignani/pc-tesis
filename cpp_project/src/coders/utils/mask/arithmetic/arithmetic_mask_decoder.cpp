
#include "arithmetic_mask_decoder.h"

#if MASK_MODE == 3

#include "decompressor.h"
#include "decoder_input.h"
#include "decoder_output.h"
#include "modelA.h"

Mask* ArithmeticMaskDecoder::decode(DecoderBase* decoder){
    Mask* mask = new Mask();
    DecoderInput input(decoder->input_file);
    DecoderOutput output(mask, decoder->data_rows_count);
    modelA<int, 16, 14> model;

    std::cout << "D1 >> decoder->flushByte();" << std::endl;
    decoder->flushByte();
    std::cout << "D1 >> decoder->flushByte();" << std::endl;

    decompress(input, output, model);

    output.close();
    mask->reset();
    return mask;
}

#endif // MASK_MODE == 3
