
#include "decoder_base.h"

#include "header_decoder.h"
#include "string_utils.h"


DecoderBase::DecoderBase(BitStreamReader* input_file_, CSVWriter* output_csv_){
    input_file = input_file_;
    output_csv = output_csv_;
}

void DecoderBase::decodeDataRowsCount(){
    data_rows_count = input_file->getInt(24); // 24 bits for the data rows count
}

std::string DecoderBase::decodeValue(int y){
    if (y == dataset->nan()) { return Constants::NO_DATA; }

    y -= dataset->offset();
    if (dataset->insideRange(y)) { return StringUtils::intToString(y); }

    throw std::invalid_argument(StringUtils::intToString(y));
}

int DecoderBase::decodeRaw(){
    return input_file->getInt(dataset->bits());
}

bool DecoderBase::decodeBool(){
    if (input_file->getBit()) { return true; } else { return false; }
}

int DecoderBase::decodeInt(int bits){
    return (input_file->getInt(bits));
}

std::string DecoderBase::decodeValueRaw(){
    int value = decodeRaw();
    std::string coded_value;
    try {
        coded_value = decodeValue(value);
    }
    catch( const std::invalid_argument& e ){
        std::cout << e.what() << std::endl;
        exit(-1);
    }
    return coded_value;
}

float DecoderBase::decodeFloat(){
    return input_file->getFloat();
}

void DecoderBase::decodeFile(){
    dataset = HeaderDecoder(input_file, output_csv).decodeHeader();
    decodeDataRowsCount();
    decodeDataRows();
}

void DecoderBase::close(){
    delete input_file;
    delete output_csv;
}

void DecoderBase::transposeMatrix(int data_rows_count_, std::vector<std::vector<std::string>> columns, int total_columns){
    for(int row_index_ = 0; row_index_ < data_rows_count_; row_index_++){
        std::vector<std::string> row;
        for(int column_index_ = 0; column_index_ < total_columns; column_index_++) {
            row.push_back(columns[column_index_][row_index_]);
        }
        output_csv->writeRowDecoder(row);
    }
}
