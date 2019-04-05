
#include "decoder_input.h"
#include <iostream>

DecoderInput::DecoderInput(BitStreamReader* input_file_){
    input_file = input_file_;
    print_ = true;
    bit_count = 1;
    byte_count = 1;
    byte_count_start = 1000000;
}

int DecoderInput::get_bit(){
    int bit = input_file->getBit();

    if (byte_count >= byte_count_start){
        std::cout << "[" << byte_count << "=" << bit_count << "] " << (bit ? "1" : "0") << std::endl;
    }
    if (bit_count % 8 == 0){
        byte_count++;
        bit_count = 0;
    }
    bit_count++;

    return bit;
}

void DecoderInput::print(){
    print_ = true;
}

void DecoderInput::setByteCount(int byte_count_){
    byte_count_start = byte_count_;
}