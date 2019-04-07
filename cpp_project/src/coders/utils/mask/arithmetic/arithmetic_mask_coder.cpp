
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
    CoderInput input(coder->input_csv, column_index);
    CoderOutput output(coder);
    modelKT<int, 16, 14> model;
    compress(input, output, model);
    flush();
    return input.total_data_rows;
}

void ArithmeticMaskCoder::flush(){
    // std::cout << "C1 >> coder->flushByte();" << std::endl;
    coder->flushByte();
    // std::cout << "C1 >> coder->flushByte();" << std::endl;
}

#endif // MASK_MODE == 3
