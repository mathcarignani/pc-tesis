
#include "coders/utils/mask/arithmetic/coder_output.h"
#include "tests_utils.h"

CoderOutput::CoderOutput(BitStreamWriter* writer_){
    writer = writer_;
}

void CoderOutput::put_bit(bool bit){
//    std::cout << "          (?) write bit = " << (bit ? "1" : "0") << std::endl;
    writer->pushBit(bit ? 1 : 0);
}
