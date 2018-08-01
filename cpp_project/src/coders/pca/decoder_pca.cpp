
#include "decoder_pca.h"

void DecoderPCA::setCoderParams(int fixed_window_size_){
    fixed_window_size = fixed_window_size_;
}

std::vector<std::string> DecoderPCA::decodeDataColumn(){
    if (Constants::MASK_MODE) { return decodeDataColumnMaskMode(); }
    else                      { return decodeDataColumnNoMask(); }
}

/// !Constants::MASK_MODE //////////////////////////////////////////////////////////////////////////////////////////////

std::vector<std::string> DecoderPCA::decodeDataColumnNoMask(){
    std::cout << "decodeDataColumnNoMask";
    std::vector<std::string> column;
    row_index = 0;
//    int unprocessed_rows = data_rows_count;
    while (data_rows_count - row_index >= fixed_window_size){
        decodeWindow(column, fixed_window_size);
//        unprocessed_rows -= row_index;
    }
    int unprocessed_rows = data_rows_count - row_index;
    if (unprocessed_rows > 0) { decodeWindow(column, unprocessed_rows); }
    return column;
}
//
//std::vector<std::string> DecoderPCA::decodeDataColumnNoMask(){
//    std::vector<std::string> column;
//    row_index = 0;
//    int unprocessed_rows = data_rows_count;
//    while (unprocessed_rows > 0){
//        if (unprocessed_rows >= fixed_window_size) { decodeWindow(column, fixed_window_size); }
//        else                                       { decodeWindow(column, unprocessed_rows);  }
//        unprocessed_rows -= row_index;
//    }
//    return column;
//}

void DecoderPCA::decodeWindow(std::vector<std::string> & column, int window_size){
    int fi = input_file.getBit();
    if (fi){ decodeNonConstantWindow(column, window_size); }
    else {   decodeConstantWindow(column, window_size); }
}

void DecoderPCA::decodeConstantWindow(std::vector<std::string> & column, int window_size){
    std::string constant = decodeValueRaw();
    for(int i=0; i < window_size; i++){
        column.push_back(constant);
        row_index++;
    }
}

void DecoderPCA::decodeNonConstantWindow(std::vector<std::string> & column, int window_size){
    for(int i = 0; i < window_size; i++){
        std::string value = decodeValueRaw();
        column.push_back(value);
        row_index++;
    }
}

/// Constants::MASK_MODE ///////////////////////////////////////////////////////////////////////////////////////////////

std::vector<std::string> DecoderPCA::decodeDataColumnMaskMode(){
    std::vector<std::string> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;
    while (unprocessed_rows >= fixed_window_size){
        if (isNoData()) {
            column.push_back(Constants::NO_DATA);
            row_index++;
        }
        else {
            decodeWindow(column, fixed_window_size);
        }
        unprocessed_rows -= row_index;
    }
    if (unprocessed_rows > 0) { decodeWindow(column, unprocessed_rows); }
    return column;
}

void DecoderPCA::decodeWindowMaskMode(std::vector<std::string> & column, int window_size){
    int fi = input_file.getBit();
    if (fi){ decodeNonConstantWindowMaskMode(column, window_size); }
    else {   decodeConstantWindowMaskMode(column, window_size); }
}

void DecoderPCA::decodeConstantWindowMaskMode(std::vector<std::string> & column, int window_size){
    std::string constant = decodeValueRaw();
    int i = 0;
    while (i < window_size){
        if (isNoData()) {
            column.push_back(Constants::NO_DATA);
        }
        else {
            column.push_back(constant);
            i++;
        }
        row_index++;
    }
}

void DecoderPCA::decodeNonConstantWindowMaskMode(std::vector<std::string> & column, int window_size){
    int i = 0;
    while (i < window_size){
        if (isNoData()) {
            column.push_back(Constants::NO_DATA);
        }
        else {
            std::string value = decodeValueRaw();
            column.push_back(value);
            i++;
        }
        row_index++;
    }
}
