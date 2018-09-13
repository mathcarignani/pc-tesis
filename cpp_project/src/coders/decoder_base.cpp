
#include "decoder_base.h"

#include "header_decoder.h"
#include "string_utils.h"


void DecoderBase::decodeDataRowsCount(){
    data_rows_count = input_file.getInt(24); // 24 bits for the data rows count
}

std::string DecoderBase::decodeValue(int y){
    if (y == dataset.nan()) { return Constants::NO_DATA; }

    y -= dataset.offset();
    if (dataset.insideRange(y)) { return StringUtils::intToString(y); }

    throw std::invalid_argument(StringUtils::intToString(y));
}

int DecoderBase::decodeRaw(){
    return input_file.getInt(dataset.bits());
}

bool DecoderBase::decodeBool(){
    if (input_file.getBit()) { return true; } else { return false; }
}

int DecoderBase::decodeInt(int bits){
    return (input_file.getInt(bits));
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
    return input_file.getFloat();
}

void DecoderBase::decodeFile(){
    dataset = HeaderDecoder(input_file, output_csv).decodeHeader();
    decodeDataRowsCount();
    decodeDataRows();
}

void DecoderBase::close(){
    input_file.~BitStreamReader();
    output_csv.close();
}
