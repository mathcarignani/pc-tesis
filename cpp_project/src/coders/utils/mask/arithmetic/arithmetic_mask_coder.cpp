
#include "arithmetic_mask_coder.h"
#include "compressor.h"
#include "coder_input.h"
#include "coder_output.h"
#include "modelA.h"

int ArithmeticMaskCoder::code(CoderBase *coder, int column_index){
//    coder->completeByte();
    CoderInput input(coder->input_csv, column_index);
    CoderOutput output(coder);
    modelA<int, 16, 14> model;

    compress(input, output, model);
    std::cout << "total_data_rows = " << input.total_data_rows << std::endl;
    return input.total_data_rows;
}
