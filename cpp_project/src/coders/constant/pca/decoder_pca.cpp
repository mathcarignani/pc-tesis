
#include "decoder_pca.h"
#include "assert.h"

std::vector<std::string> DecoderPCA::decodeDataColumn(){
    std::vector<std::string> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;

#if MASK_MODE && CHECKS
    assert(mask->total_no_data + mask->total_data == data_rows_count);
#endif

    while (unprocessed_rows > 0) {
    #if MASK_MODE
        if (mask->isNoData()) {
            column.push_back(Constants::NO_DATA);
            row_index++; unprocessed_rows--;
            continue;
        }
        int w_size = window_size;
        if (mask->total_data < w_size) { w_size = mask->total_data; }
        decodeWindow(column, w_size);
    #else
        int w_size = window_size;
        if (unprocessed_rows < w_size) { w_size = unprocessed_rows; }
        decodeWindow(column, w_size);
    #endif
        unprocessed_rows = data_rows_count - row_index;
    }
    return column;
}

void DecoderPCA::decodeWindow(std::vector<std::string> & column, int window_size){
    int fi = input_file->getBit();
    if (fi){ decodeNonConstantWindow(column, window_size); }
    else {   decodeConstantWindow(this, column, window_size); }
#if MASK_MODE
    mask->total_data -= window_size;
#endif
}

void DecoderPCA::decodeConstantWindow(DecoderBase* decoder, std::vector<std::string> & column, int window_size){
    std::string constant = decoder->decodeValueRaw();
    int i = 0;
    while (i < window_size){
    #if MASK_MODE
        if (i > 0 && decoder->mask->isNoData()) { // always false in the first iteration
            column.push_back(Constants::NO_DATA);
            decoder->row_index++;
            continue;
        }
    #endif
        column.push_back(constant);
        i++;
        decoder->row_index++;
    }
}

void DecoderPCA::decodeNonConstantWindow(std::vector<std::string> & column, int window_size){
    int i = 0;
    while (i < window_size){
    #if MASK_MODE
        if (i > 0 && mask->isNoData()) { // always false in the first iteration
            column.push_back(Constants::NO_DATA);
            row_index++;
            continue;
        }
    #endif
        std::string value = decodeValueRaw();
        column.push_back(value);
        i++;
        row_index++;
    }
}
