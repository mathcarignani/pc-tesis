
#include "decoder_pca.h"

#include "assert.h"

void DecoderPCA::setCoderParams(int fixed_window_size_){
    fixed_window_size = fixed_window_size_;
}

std::vector<std::string> DecoderPCA::decodeDataColumn(){
    if (Constants::MASK_MODE) { return decodeDataColumnMaskMode(); }
    else                      { return decodeDataColumnNoMask(); }
}

/// !Constants::MASK_MODE //////////////////////////////////////////////////////////////////////////////////////////////

std::vector<std::string> DecoderPCA::decodeDataColumnNoMask(){
    std::vector<std::string> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;
    while (unprocessed_rows > 0) {
        int w_size = fixed_window_size;
        if (unprocessed_rows < w_size) { w_size = unprocessed_rows; }
        decodeWindow(column, w_size);
        unprocessed_rows = data_rows_count - row_index;
    }
    return column;
}

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
    std::cout << "decodeDataColumnMaskMode size = " << burst_is_no_data_vector.size() << std::endl;
    std::cout << "total_no_data + total_data = " << total_no_data << " + " << total_data << " = " << data_rows_count << " = data_rows_count" << std::endl;
    assert(total_no_data + total_data == data_rows_count);
    std::vector<std::string> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;
    while (unprocessed_rows > 0){
        if (isNoData()) {
            std::cout << "no data row index =" << row_index << std::endl;
            column.push_back(Constants::NO_DATA);
            row_index++;
        }
        else {
            int w_size = fixed_window_size;
            if (total_data < w_size) { w_size = total_data; }
            std::cout << "1" << std::endl;
            decodeWindowMaskMode(column, w_size);
            std::cout << "2" << std::endl;
        }
        unprocessed_rows = data_rows_count - row_index;
        std::cout << "unprocessed_rows=" << unprocessed_rows << std::endl;
    }
    return column;
}

void DecoderPCA::decodeWindowMaskMode(std::vector<std::string> & column, int window_size){
    int fi = input_file.getBit();
    if (fi){ decodeNonConstantWindowMaskMode(column, window_size); }
    else {   decodeConstantWindowMaskMode(column, window_size); }
    total_data -= window_size;
}

void DecoderPCA::decodeConstantWindowMaskMode(std::vector<std::string> & column, int window_size){
    std::string constant = decodeValueRaw();
    int i = 0;
    while (i < window_size){
        if (i > 0 && isNoData()) {
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
        if (i > 0 && isNoData()) { // always false in the first iteration
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
