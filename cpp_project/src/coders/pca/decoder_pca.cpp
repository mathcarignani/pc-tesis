
#include "decoder_pca.h"

void DecoderPCA::setCoderParams(int fixed_window_size_){
    fixed_window_size = fixed_window_size_;
}

std::vector<std::string> DecoderPCA::decodeDataColumn(){
    std::vector<std::string> column;
    row_index = 0;
    while (data_rows_count - row_index >= fixed_window_size){
        decodeWindow(column, fixed_window_size);
    }
    int unprocessed_rows = data_rows_count - row_index;
    if (unprocessed_rows > 0) { decodeWindow(column, unprocessed_rows); }
    return column;
}

void DecoderPCA::decodeWindow(std::vector<std::string> & column, int window_size){
    int fi = input_file.getBit();
    if (fi){
        for(int i = 0; i < window_size; i++){
            std::string value = decodeValueRaw();
            column.push_back(value);
            row_index++;
        }
    }
    else {
        std::string constant = decodeValueRaw();
        for(int i=0; i < window_size; i++){
            column.push_back(constant);
            row_index++;
        }
    }
}
