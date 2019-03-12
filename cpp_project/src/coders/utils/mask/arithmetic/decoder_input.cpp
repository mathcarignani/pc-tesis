
#include "decoder_input.h"
#include <iostream>

DecoderInput::DecoderInput(BitStreamReader* input_file_){
    input_file = input_file_;
}

int DecoderInput::get_bit(){
    int bit = input_file->getBit(); // TODO: getBitOther();
//    std::cout << "DecoderInput::get_bit() => " << (bit ? "1" : "0") << std::endl;
    return bit;
}
