
#include "decoder_output.h"

DecoderOutput::DecoderOutput(Mask* mask_){
    mask = mask_;
    row_index = 0;
}

void DecoderOutput::putByte(int c){
    bool nodata = c == 1;

    if (row_index == 0){
        burst = new Burst(nodata);
    }
    else if (nodata == burst->no_data) {
        burst->increaseLength();
    }
    else {
        mask->add(burst);
        burst = new Burst(nodata);
    }
    row_index++;
}

void DecoderOutput::close(){
    mask->add(burst);
}
