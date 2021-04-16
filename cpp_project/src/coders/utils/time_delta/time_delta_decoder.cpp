
#include "time_delta_decoder.h"
#include "conversor.h"
#include "decoder_apca.h"

std::vector<std::string> TimeDeltaDecoder::decode(DecoderCommon* decoder){
    bool mask_mode = false;
    std::vector<std::string> column = DecoderAPCA::decodeDataColumn(decoder, mask_mode);

    for (int i=0; i < column.size(); i++){
        std::string value = column.at(i);
        int value_int = Conversor::stringToInt(value);
        decoder->time_delta_vector.push_back(value_int);
    }
    return column;
}
