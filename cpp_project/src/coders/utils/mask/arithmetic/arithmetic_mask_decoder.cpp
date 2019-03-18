
#include "arithmetic_mask_decoder.h"

#if MASK_MODE == 3

#include "decompressor.h"
#include "decoder_input.h"
#include "decoder_output.h"
#include "modelKT.h"

Mask* ArithmeticMaskDecoder::decode(DecoderBase* decoder){
    std::cout << "D1 >> decoder->flushByte();" << std::endl;
    decoder->flushByte();
    std::cout << "D1 >> decoder->flushByte();" << std::endl;

    Mask* mask = new Mask();
    DecoderInput input(decoder->input_file);
    DecoderOutput output(mask, decoder->data_rows_count);
    modelKT<int, 16, 14> model;

    decompress(input, output, model);

    std::cout << "D1 >> decoder->flushByte();" << std::endl;
    decoder->flushByte();
    std::cout << "D1 >> decoder->flushByte();" << std::endl;

    output.close();
    mask->reset();
    return mask;
}

#endif // MASK_MODE == 3
