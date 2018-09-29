
#include "decoder_pca.h"
#include "assert.h"

void DecoderPCA::setCoderParams(int fixed_window_size_){
    fixed_window_size = fixed_window_size_;
}

std::vector<std::string> DecoderPCA::decodeDataColumn(){
    std::vector<std::string> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;

#if MASK_MODE
    assert(total_no_data + total_data == data_rows_count);
#endif

    while (unprocessed_rows > 0) {
    #if MASK_MODE
        if (isNoData()) {
            column.push_back(Constants::NO_DATA);
            row_index++; unprocessed_rows--;
            continue;
        }
        int w_size = fixed_window_size;
        if (total_data < w_size) { w_size = total_data; }
        decodeWindow(column, w_size);
    #else
        int w_size = fixed_window_size;
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
    else {   decodeConstantWindow(column, window_size); }
#if MASK_MODE
    total_data -= window_size;
#endif
}

void DecoderPCA::decodeConstantWindow(std::vector<std::string> & column, int window_size){
    std::string constant = decodeValueRaw();
    int i = 0;
    while (i < window_size){
    #if MASK_MODE
        if (i > 0 && isNoData()) { // always false in the first iteration
            column.push_back(Constants::NO_DATA);
            row_index++;
            continue;
        }
    #endif
        column.push_back(constant);
        i++;
        row_index++;
    }
}

void DecoderPCA::decodeNonConstantWindow(std::vector<std::string> & column, int window_size){
    int i = 0;
    while (i < window_size){
    #if MASK_MODE
        if (i > 0 && isNoData()) { // always false in the first iteration
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
