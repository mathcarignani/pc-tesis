
#include "coder_base.h"

#include "header_coder.h"


void CoderBase::codeDataRowsCount(){
    int data_rows_count = input_csv.total_lines - 4;
    output_file.pushInt(data_rows_count, 24); // 24 bits for the data rows count
}

//
// This method maps a value read in the csv file into an integer to be written in the output file.
// It also checks the minimum and maximum constraints.
//
int CoderBase::codeValue(std::string x){
    if (x[0] == 'N'){ return dataset.nan(); }

    int x_int = std::stoi(x);
    if (dataset.insideRange(x_int)) { return x_int + dataset.offset(); }

    throw std::invalid_argument(std::to_string(x_int));
}

void CoderBase::codeRaw(int value){
    output_file.pushInt(value, dataset.getBits());
}

void CoderBase::codeBit(int bit){
    dataset.addBits(1);
    output_file.pushBit(bit);
}

void CoderBase::codeValueRaw(std::string x){
    int value;
    try {
        value = codeValue(x);
    }
    catch( const std::invalid_argument& e ){
        std::cout << "STRING OUT OF DATASET RANGE = " << e.what() << std::endl;
        exit(-1);
    }
    codeRaw(value);
}

void CoderBase::codeFile(){
    dataset = HeaderCoder(input_csv, output_file).codeHeader();
    codeDataRowsCount();
    codeDataRows();
}

void CoderBase::printBits(){
    dataset.printBits();
}

void CoderBase::close(){
    input_csv.close();
    output_file.~BitStreamWriter();
}
