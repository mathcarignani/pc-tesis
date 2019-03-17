
#include "arithmetic_mask_coder.h"

#if MASK_MODE == 3

#include "compressor.h"
#include "coder_input.h"
#include "coder_output.h"
#include "modelA.h"

#include "tests_utils.h"
#include "decoder_input.h"
#include "decoder_output.h"
#include "decompressor.h"

int ArithmeticMaskCoder::code(CoderBase *coder, int column_index){
    std::cout << "C1 >> coder->flushByte();" << std::endl;
    coder->flushByte();
    std::cout << "C1 >> coder->flushByte();" << std::endl;

    // compress with arithmetic coder routine
    Path path = Path(TestsUtils::OUTPUT_PATH, "algo.bin");
    BitStreamWriter* writer = new BitStreamWriter(path);

    CoderInput input_coder(coder->input_csv, column_index);
    CoderOutput output_coder(writer);
    modelA<int, 16, 14> model1;
    compress(input_coder, output_coder, model1);
    // writer->flushByte();
    delete writer;

    // decompress with arithmetic decoder routine
    BitStreamReader* reader = new BitStreamReader(path);
    DecoderInput input_decoder(reader);
    Mask* mask = new Mask();
    DecoderOutput output_decoder(mask, coder->data_rows_count);
    modelA<int, 16, 14> model2;
    decompress(input_decoder, output_decoder, model2);
    int total_bytes = reader->current_byte;
    if (reader->current_unread) { total_bytes--; }
    std::cout << "total_bytes = " << total_bytes << std::endl;
    delete reader;

    // just copy the necessary bytes
    reader = new BitStreamReader(path);
    for(int i=0; i < total_bytes; i++){
        int value = reader->getInt(8);
        coder->codeInt(value, 8);
    }
    coder->flushByte();

//    std::cout << "C1 >> coder->flushByte();" << std::endl;
//    coder->flushByte();
//    std::cout << "C1 >> coder->flushByte();" << std::endl;
//    exit(1);
    return input_coder.total_data_rows;
}

#endif // MASK_MODE == 3
