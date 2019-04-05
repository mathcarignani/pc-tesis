
#include "coders/utils/mask/arithmetic/coder_output.h"
#include "tests_utils.h"

CoderOutput::CoderOutput(BitStreamWriter* writer_){
    writer = writer_;
    print_ = false;
    byte_count = 1;
    bit_count = 1;
}

void CoderOutput::put_bit(bool bit){
    writer->pushBit(bit ? 1 : 0);

    if (print_){
        std::cout << "[" << byte_count << "=" << bit_count << "] " << (bit ? "1" : "0") << std::endl;
    }
    if (bit_count % 8 == 0){
        byte_count++;
        bit_count = 0;
    }
    bit_count++;

}

void CoderOutput::print(){
    print_ = true;
}
