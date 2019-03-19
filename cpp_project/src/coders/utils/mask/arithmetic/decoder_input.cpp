
#include "decoder_input.h"
#include <iostream>

DecoderInput::DecoderInput(BitStreamReader* input_file_){
    input_file = input_file_;
}

int DecoderInput::get_bit(){
    int bit = input_file->getBit();
    return bit;
}
