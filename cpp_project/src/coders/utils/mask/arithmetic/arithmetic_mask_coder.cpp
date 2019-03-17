
#include "arithmetic_mask_coder.h"

#if MASK_MODE == 3

#include "compressor.h"
#include "coder_input.h"
#include "coder_output.h"
#include "modelA.h"

int ArithmeticMaskCoder::code(CoderBase *coder, int column_index){
    CoderInput input(coder->input_csv, column_index);
    CoderOutput output(coder);
    modelA<int, 16, 14> model;

    std::cout << "C1 >> coder->flushByte();" << std::endl;
    coder->flushByte();
    std::cout << "C1 >> coder->flushByte();" << std::endl;

    compress(input, output, model);

    std::cout << "C1 >> coder->flushByte();" << std::endl;
    coder->flushByte();
    std::cout << "C1 >> coder->flushByte();" << std::endl;

    return input.total_data_rows;
}

#endif // MASK_MODE == 3
