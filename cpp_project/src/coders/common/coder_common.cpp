
#include "coder_common.h"

#include "header_coder.h"
#include "conversor.h"
#include "assert.h"
#include <math.h>
#include "coder_utils.h"

CoderCommon::CoderCommon(CSVReader* input_csv_, BitStreamWriter* output_file_){
   input_csv = input_csv_;
   output_file = output_file_;
   dataset = new Dataset();
}

void CoderCommon::codeDataRowsCount(){
    data_rows_count = input_csv->total_lines - HeaderCoder::HEADER_LINES;
#if CHECKS
    assert(0 < data_rows_count && data_rows_count < pow(2, 24));
#endif
    codeInt(data_rows_count, 24); // 24 bits for the data rows count
}

//
// This method maps a value read in the csv file into an integer to be written in the output file.
// It also checks the minimum and maximum constraints.
//
int CoderCommon::codeValue(std::string x){
    std::string unmapped_x = CoderUtils::unmapValue(x, 0);

    if (Constants::isNoData(x)){ return dataset->nan(); }

    int x_int = Conversor::stringToInt(x);
    if (dataset->insideRange(x_int)) { return x_int + dataset->offset(); }

    throw std::invalid_argument(Conversor::intToString(x_int));
}

void CoderCommon::codeRaw(int value){
    output_file->pushInt(value, dataset->getBits());
}

void CoderCommon::codeBit(int bit){
    dataset->addBits(1);
    output_file->pushBit(bit);
}

void CoderCommon::codeBits(int bit, int times){
    dataset->addBits(times);
    output_file->pushBits(bit, times);
}

void CoderCommon::codeBool(bool bit){
    dataset->addBits(1);
    if (bit) { output_file->pushBit(1); }
    else     { output_file->pushBit(0); }
}

void CoderCommon::codeInt(int value, int bits){
    dataset->addBits(bits);
    output_file->pushInt(value, bits);
}

void CoderCommon::codeWindowLength(Window* window){
    codeInt(window->length - 1, window->window_size_bit_length);
}

void CoderCommon::codeUnary(int value){
    for(int i=0; i < value; i++) { codeBit(0); }
    codeBit(1);
}

void CoderCommon::codeValueRaw(std::string x){
    int value;
    try {
        value = codeValue(x);
        // std::cout << "codeValue(" << x << ") = " << value << std::endl;
    }
    catch( const std::invalid_argument& e ){
        std::cout << "CoderCommon::codeValueRaw: " << e.what() << std::endl;
        delete input_csv;
        delete output_file;
        exit(-1);
    }
    codeRaw(value);
}

void CoderCommon::codeFloat(float x){
    dataset->addBits(sizeof(float)*8);
    output_file->pushFloat(x);
}

void CoderCommon::codeDouble(double x){
    dataset->addBits(sizeof(double)*8);
    output_file->pushDouble(x);
}

void CoderCommon::flushByte(){
    int remaining = output_file->flushByte();
    dataset->addBits(remaining);
}

void CoderCommon::codeFile(){
    codeCoderParams();
    HeaderCoder(input_csv, this).codeHeader(dataset);
    codeDataRowsCount();
    codeDataRows();
}

void CoderCommon::codeCoderParameters(int coder_code, int window_size){
    assert(0 <= coder_code && coder_code < pow(2, 8));
    codeInt(coder_code, 8); // 8 bits for the coder_code

    assert(1 <= window_size && window_size <= pow(2, 8));
    codeInt(window_size - 1, 8); // 8 bits for the window_size
}

void CoderCommon::printBits(){
    dataset->printBits();
}

void CoderCommon::close(){
    delete input_csv;
    delete output_file;
}
