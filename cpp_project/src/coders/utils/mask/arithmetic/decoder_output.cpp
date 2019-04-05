
#include "decoder_output.h"

DecoderOutput::DecoderOutput(Mask* mask_, int data_rows_count_){
    mask = mask_;
    data_rows_count = data_rows_count_;
    row_index = 0;
}

int DecoderOutput::putByte(int c){
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
    // std::cout << "[" << row_index << "] >>>>>>>>>>>>>>>>>>> DecoderOutput = " << c << std::endl;
    row_index++;
    data_rows_count--;
    return data_rows_count;
}

void DecoderOutput::close(){
    mask->add(burst);
}
