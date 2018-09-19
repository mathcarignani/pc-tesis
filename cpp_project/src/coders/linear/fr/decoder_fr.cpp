
#include "decoder_fr.h"
#include "math_utils.h"
#include "assert.h"
#include "DataItem.h"
#include "string_utils.h"

void DecoderFR::setCoderParams(int max_window_size_){
    max_window_size = max_window_size_;
    max_window_size_bit_length = MathUtils::bitLength(max_window_size_);
}

std::vector<std::string> DecoderFR::decodeDataColumn(){
    std::vector<std::string> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;

#if MASK_MODE
    assert(total_no_data + total_data == data_rows_count);
#endif

    while (unprocessed_rows > 0){
    #if MASK_MODE
        if (isNoData()) {
            column.push_back(Constants::NO_DATA);
            row_index++; unprocessed_rows--;
            continue;
        }
        int w_size = (total_data < max_window_size) ? total_data : max_window_size;
        decodeWindow(column, w_size);
    #else
        // TODO: not implemented
    #endif
        unprocessed_rows = data_rows_count - row_index;
    }
    return column;
}

void DecoderFR::decodeWindow(std::vector<std::string> & column, int window_size){
    std::vector<DataItem> window;
    window.reserve(window_size);
    for(int i=0; i < window_size; i++){
        std::string value_str = decodeValueRaw();
        int value = StringUtils::stringToInt(value_str);
        int index = (i == 0) ? 0 : decodeInt(max_window_size_bit_length);
        window[i] = DataItem(value, index);
    }

    ///////////////////// TODO

//    int i = 0;
//    while (i < window_size){
//    #if MASK_MODE
//        if (i > 0 && isNoData()) { // always false in the first iteration
//            column.push_back(Constants::NO_DATA);
//            row_index++;
//            continue;
//        }
//    #endif
//        std::string value = decodeValueRaw();
//        column.push_back(value);
//        i++;
//        row_index++;
//    }
#if MASK_MODE
    total_data -= window_size;
#endif
}

