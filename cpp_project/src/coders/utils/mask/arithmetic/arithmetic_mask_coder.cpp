
#include "arithmetic_mask_coder.h"

#if MASK_MODE == 3

#include "compressor.h"
#include "coder_input.h"
#include "coder_output.h"
#include "modelKT.h"

#include "tests_utils.h"
#include "decoder_input.h"
#include "decoder_output.h"
#include "decompressor.h"

ArithmeticMaskCoder::ArithmeticMaskCoder(CoderBase* coder_, int column_index_){
    coder = coder_;
    column_index = column_index_;
}

int ArithmeticMaskCoder::code(){
    flush();
    Path path = Path(TestsUtils::OUTPUT_PATH, "temp.bin");
    int total_data_rows = callCompress(path);
    int total_bytes = callDecompress(path);
    copyBytes(path, total_bytes); // only copy the necessary bytes
    flush();
    return total_data_rows;
}

void ArithmeticMaskCoder::flush(){
    // std::cout << "C1 >> coder->flushByte();" << std::endl;
    coder->flushByte();
    // std::cout << "C1 >> coder->flushByte();" << std::endl;
}

int ArithmeticMaskCoder::callCompress(Path path){
    std::cout << "callCompress" << std::endl;
    CoderInput input(coder->input_csv, column_index);
    BitStreamWriter* writer = new BitStreamWriter(path);
    CoderOutput output(writer);
    modelKT<int, 16, 14> model;

    compress(input, output, model);

    // writer->flushByte();
    byte_count = output.byte_count;
    delete writer;
    return input.total_data_rows;
}

int ArithmeticMaskCoder::callDecompress(Path path){
    std::cout << "callDecompress" << std::endl;
    BitStreamReader* reader = new BitStreamReader(path);
    DecoderInput input(reader);
    input.setByteCount(byte_count);
    Mask* mask = new Mask();
    DecoderOutput output(mask, coder->data_rows_count);
    modelKT<int, 16, 14> model;

    decompress(input, output, model);

    int total_bytes = reader->current_byte;
    if (reader->current_unread) { total_bytes--; }
    delete reader;
    return total_bytes;
}

void ArithmeticMaskCoder::copyBytes(Path path, int total_bytes){
    std::cout << "copyBytes" << std::endl;
    int diff = total_bytes - byte_count;
    std::cout << "difff = " << diff << ", byte_count = " << byte_count << ", decodedBytes = " << total_bytes << std::endl;
    BitStreamReader* reader = new BitStreamReader(path);
    for(int i=0; i < total_bytes; i++){
        int value = reader->getInt(8);
        coder->codeInt(value, 8);
    }
}

#endif // MASK_MODE == 3
