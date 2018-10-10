
#include "decoder_apca.h"
#include "assert.h"
#include "math_utils.h"

void DecoderAPCA::setCoderParams(int max_window_size_){
    max_window_size_bit_length = MathUtils::bitLength(max_window_size_);
}

std::vector<std::string> DecoderAPCA::decodeDataColumn(){
    std::vector<std::string> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;

#if MASK_MODE && CHECKS
    assert(mask->total_no_data + mask->total_data == data_rows_count);
#endif

    while (unprocessed_rows > 0) {
   #if MASK_MODE
        if (isNoData()) {
            column.push_back(Constants::NO_DATA);
            row_index++; unprocessed_rows--;
            continue;
        }
   #endif
        decodeWindow(column);
        unprocessed_rows = data_rows_count - row_index;
    }
    return column;
}

void DecoderAPCA::decodeWindow(std::vector<std::string> & column){
    int window_size = input_file->getInt(max_window_size_bit_length);
    DecoderPCA::decodeConstantWindow(column, window_size);
#if MASK_MODE
    mask->total_data -= window_size;
#endif
}
