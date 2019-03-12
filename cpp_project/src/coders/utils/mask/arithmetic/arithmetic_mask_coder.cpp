
#include "arithmetic_mask_coder.h"

#if MASK_MODE == 3

#include "compressor.h"
#include "coder_input.h"
#include "coder_output.h"
#include "modelA.h"

int ArithmeticMaskCoder::code(CoderBase *coder, int column_index){
//    std::cout << "C >> coder->flushByte();" << std::endl;
//    std::cout << "coder->flushByte();" << std::endl;
//    coder->flushByte();
//    std::cout << "C >> coder->flushByte();" << std::endl;
    int bits_before = coder->dataset->total_bits;
    CoderInput input(coder->input_csv, column_index);
    CoderOutput output(coder);
    modelA<int, 16, 14> model;

    compress(input, output, model);
//    std::cout << "C << coder->flushByte();" << std::endl;
//    coder->flushByte();
//    std::cout << "C << coder->flushByte();" << std::endl;
//    int bits_after = coder->dataset->total_bits;
//    for(int i=0; i < bits_after - bits_before; i++)
//        coder->codeBool(false);
    return input.total_data_rows;
}

#endif // MASK_MODE == 3
