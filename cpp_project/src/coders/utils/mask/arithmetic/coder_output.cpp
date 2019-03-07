
#include "coders/utils/mask/arithmetic/coder_output.h"

CoderOutput::CoderOutput(CoderBase* coder_){
    coder = coder_;
}

void CoderOutput::put_bit(bool bit){
//    std::cout << "codeBool(" << (bit ? "1" : "0") << ")" << std::endl;
    coder->codeBool(bit);
}
