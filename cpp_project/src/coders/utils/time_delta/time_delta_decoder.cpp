
#include "time_delta_decoder.h"
#include "string_utils.h"

//
// TODO: use a more appropriate lossless compression schema for coding the time delta column.
//
std::vector<std::string> TimeDeltaDecoder::decode(DecoderBase* decoder){
    std::vector<std::string> column;

    for(int row_index = 0; row_index < decoder->data_rows_count; row_index++){
        std::string value = decoder->decodeValueRaw();
        column.push_back(value);

        // add int value to the time_delta_vector
        int value_int = StringUtils::stringToInt(value);
        decoder->time_delta_vector.push_back(value_int);
    }
    return column;
}
