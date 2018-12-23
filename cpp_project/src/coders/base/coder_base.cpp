
#include "coder_base.h"

#include "header_coder.h"
#include "string_utils.h"
#include "assert.h"
#include <math.h>

CoderBase::CoderBase(CSVReader* input_csv_, BitStreamWriter* output_file_){
   input_csv = input_csv_;
   output_file = output_file_;
}

void CoderBase::codeDataRowsCount(){
    int data_rows_count = input_csv->total_lines - HeaderCoder::HEADER_LINES;
    assert(0 < data_rows_count && data_rows_count < pow(2, 24));
    output_file->pushInt(data_rows_count, 24); // 24 bits for the data rows count
}

//
// This method maps a value read in the csv file into an integer to be written in the output file.
// It also checks the minimum and maximum constraints.
//
int CoderBase::codeValue(std::string x){
    if (Constants::isNoData(x)){ return dataset->nan(); }

    int x_int = StringUtils::stringToInt(x);
    if (dataset->insideRange(x_int)) { return x_int + dataset->offset(); }

    throw std::invalid_argument(StringUtils::intToString(x_int));
}

void CoderBase::codeRaw(int value){
    output_file->pushInt(value, dataset->getBits());
}

void CoderBase::codeBit(int bit){
    dataset->addBits(1);
    output_file->pushBit(bit);
}

void CoderBase::codeBool(bool bit){
    dataset->addBits(1);
    if (bit) { output_file->pushBit(1); }
    else     { output_file->pushBit(0); }
}

void CoderBase::codeInt(int value, int bits){
    dataset->addBits(bits);
    output_file->pushInt(value, bits);
}

void CoderBase::codeValueRaw(std::string x){
    int value;
    try {
        value = codeValue(x);
    }
    catch( const std::invalid_argument& e ){
        std::cout << "CoderBase::codeValueRaw: " << e.what() << std::endl;
        exit(-1);
    }
    codeRaw(value);
}

void CoderBase::codeFloat(float x){
    dataset->addBits(sizeof(float)*8);
    output_file->pushFloat(x);
}

void CoderBase::codeDouble(double x){
    dataset->addBits(sizeof(double)*8);
    output_file->pushDouble(x);
}

void CoderBase::codeFile(){
    codeCoderParams();
    dataset = HeaderCoder(input_csv, output_file).codeHeader();
    codeDataRowsCount();
    codeDataRows();
}

void CoderBase::codeCoderParameters(int coder_code, int window_size){
    assert(0 <= coder_code && coder_code < pow(2, 8));
    output_file->pushInt(coder_code, 8); // 8 bits for the coder_code

    assert(1 <= window_size && window_size < pow(2, 8));
    output_file->pushInt(window_size, 8); // 8 bits for the window_size
}

void CoderBase::printBits(){
    dataset->printBits();
}


void CoderBase::close(){
    delete input_csv;
    delete output_file;
}
