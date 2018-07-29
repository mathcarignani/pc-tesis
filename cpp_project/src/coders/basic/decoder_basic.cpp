
#include "decoder_basic.h"

std::vector<std::string> DecoderBasic::decodeDataColumn(){
    std::vector<std::string> column;
    for(int row_index = 0; row_index < data_rows_count; row_index++){
        std::string value = decodeValueRaw();
        column.push_back(value);
    }
    return column;
}
