
#include "decoder_apca.h"
#include "assert.h"
#include "math_utils.h"

std::vector<std::string> DecoderAPCA::decodeDataColumn(){
    return decodeDataColumn(this);
}

//
// This needs to be a static method because it is also called by DecoderGAMPS
//
std::vector<std::string> DecoderAPCA::decodeDataColumn(DecoderCommon* decoder){
    std::vector<std::string> column;
    decoder->row_index = 0;

#if MASK_MODE
#if CHECKS
    assert(decoder->mask->total_no_data + decoder->mask->total_data == decoder->data_rows_count);
#endif // END CHECKS
#endif // END MASK_MODE

    int unprocessed_rows = decoder->data_rows_count;
    while (unprocessed_rows > 0) {
#if MASK_MODE
        if (decoder->mask->isNoData()) {
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

void DecoderAPCA::decodeWindow(DecoderCommon* decoder, std::vector<std::string> & column){
    int window_size = decoder->decodeWindowLength();
    DecoderPCA::decodeConstantWindow(decoder, column, window_size);
#if MASK_MODE
    decoder->mask->total_data -= window_size;
#endif
}
