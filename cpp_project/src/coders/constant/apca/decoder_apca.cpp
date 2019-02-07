
#include "decoder_apca.h"
#include "assert.h"
#include "math_utils.h"

std::vector<std::string> DecoderAPCA::decodeDataColumn(){
    return decodeDataColumn(this);
}

std::vector<std::string> DecoderAPCA::decodeDataColumn(DecoderBase* decoder){
    std::vector<std::string> column;
    decoder->row_index = 0;
    int unprocessed_rows = decoder->data_rows_count;

#if MASK_MODE
    Mask* mask = decoder->mask;
#if CHECKS
    assert(mask->total_no_data + mask->total_data == decoder->data_rows_count);
#endif // END CHECKS
#endif // END MASK_MODE


    while (unprocessed_rows > 0) {
    #if MASK_MODE
        if (mask->isNoData()) {
            column.push_back(Constants::NO_DATA);
            decoder->row_index++; unprocessed_rows--;
            continue;
        }
    #endif
        decodeWindow(decoder, column);
        unprocessed_rows = decoder->data_rows_count - decoder->row_index;
    }
    return column;
}

void DecoderAPCA::decodeWindow(DecoderBase* decoder, std::vector<std::string> & column){
    int window_size = decoder->input_file->getInt(decoder->window_size_bit_length);
    DecoderPCA::decodeConstantWindow(decoder, column, window_size);
#if MASK_MODE
    decoder->mask->total_data -= window_size;
#endif
}
