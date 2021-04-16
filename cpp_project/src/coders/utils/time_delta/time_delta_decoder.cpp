
#include "time_delta_decoder.h"
#include "conversor.h"
#include "decoder_apca.h"

std::vector<std::string> TimeDeltaDecoder::decode(DecoderCommon* decoder){
    bool mask_mode = false;

    int window_size_bit_length = decoder->window_size_bit_length;
    decoder->setWindowSizeBitLength(8);
    std::vector<std::string> column = DecoderAPCA::decodeDataColumn(decoder, mask_mode);
    decoder->setWindowSizeBitLength(window_size_bit_length);

    for (int i=0; i < column.size(); i++){
        std::string value = column.at(i);
        int value_int = Conversor::stringToInt(value);
        decoder->time_delta_vector.push_back(value_int);
    }
    return column;
}
