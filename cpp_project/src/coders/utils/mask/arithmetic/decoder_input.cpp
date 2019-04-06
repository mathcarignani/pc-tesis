
#include "decoder_input.h"
#include <iostream>

DecoderInput::DecoderInput(BitStreamReader* input_file_){
    input_file = input_file_;
    current_burst = false; // doesn't matter
    int current_burst_count = -1;
    bool previous_burst = false;
}

int DecoderInput::get_bit(){
    int bit = input_file->getBit();
    if (current_burst_count == -1){ // first call
        current_burst = bit;
        current_burst_count = 1;
    }
    else if (current_burst == bit){
        current_burst_count++;
        assert(current_burst_count <= 16);
    }
    else { // current_burst != bit
        if (current_burst_count == 16) {
            if (!previous_burst) {
                previous_burst = true;
                current_burst = bit;
                current_burst_count = 1;
            }
            else {
                std::cout << "THIS IS THE END..." << std::endl;
            }
        }
        else {
            previous_burst = false;
            current_burst = bit;
            current_burst_count = 1;
        }
    }
    return bit;
}

void DecoderInput::finish_decoding(){
    std::cout << "finish_decoding" << std::endl;
    while (!(previous_burst && current_burst_count == 16)){
        get_bit();
    }
}