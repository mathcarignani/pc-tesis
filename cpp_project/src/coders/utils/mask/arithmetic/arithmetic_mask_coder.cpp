
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

ArithmeticMaskCoder::ArithmeticMaskCoder(CoderBase* coder_, int data_columns_count_){
    coder = coder_;
    data_columns_count = data_columns_count_;
}

std::vector<int> ArithmeticMaskCoder::code(){
    flush();
    CoderInput input(coder, data_columns_count);
    CoderOutput output(coder);
    modelKT<int, 16, 14> model;
    compress(input, output, model);
    flush();
    return input.total_data_rows_vector;
}

void ArithmeticMaskCoder::flush(){
    // std::cout << "C1 >> coder->flushByte();" << std::endl;
    coder->flushByte();
    // std::cout << "C1 >> coder->flushByte();" << std::endl;
}

#endif // MASK_MODE == 3
