
#include "decoder_input.h"

DecoderInput::DecoderInput(BitStreamReader* input_file_){
    input_file = input_file_;
}

int DecoderInput::get_bit(){
    return input_file->getBit();
}
