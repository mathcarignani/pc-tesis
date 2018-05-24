
#include "decoder_apca.h"

#include "string_utils.h"

void DecoderAPCA::setCoderParams(int max_window_size_){
    max_window_size_bit_length = StringUtils::bitLength(max_window_size_);
}

std::vector<std::string> DecoderAPCA::decodeColumn(){
    std::vector<std::string> column;
    row_index = 0;
    while (row_index < data_rows_count){
        decodeWindow(column);
    }
    return column;
}

void DecoderAPCA::decodeWindow(std::vector<std::string> & column){
    int window_size = input_file.getInt(max_window_size_bit_length);
    std::string value = decodeValueRaw();
    for (int i=0; i < window_size; i++){
        column.push_back(value);
        row_index++;
    }
}
