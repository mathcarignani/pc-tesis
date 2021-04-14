
#include "arithmetic_mask_coder.h"

#if MASK_MODE

#include "compressor.h"
#include "coder_input.h"
#include "coder_output.h"
#include "modelKT.h"

#include "tests_utils.h"
#include "decoder_input.h"
#include "decoder_output.h"
#include "decompressor.h"

ArithmeticMaskCoder::ArithmeticMaskCoder(CoderCommon* coder_, int first_column_index_, int last_column_index_){
    coder = coder_;
    first_column_index = first_column_index_;
    last_column_index = last_column_index_;
}

std::vector<int> ArithmeticMaskCoder::code(){
    flush();
    std::vector<int> total_data_rows_vector = callCompress();
    flush();
    return total_data_rows_vector;
}

void ArithmeticMaskCoder::flush(){
    coder->flushByte();
}

std::vector<int> ArithmeticMaskCoder::callCompress(){
    CoderInput input(coder, first_column_index, last_column_index);
    CoderOutput output(coder);
    modelKT<int, 16, 14> model;
    compress(input, output, model);
    return input.total_data_rows_vector;
}

#endif // MASK_MODE
