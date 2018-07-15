
#include "decoder_base.h"

#include "header_decoder.h"


void DecoderBase::decodeDataRowsCount(){
    data_rows_count = input_file.getInt(24); // 24 bits for the data rows count
}

std::string DecoderBase::decodeValue(int y){
    if (y == dataset.nan()) { return NO_DATA; }

    y -= dataset.offset();
    if (dataset.insideRange(y)) { return std::to_string(y); }

    throw std::invalid_argument(std::to_string(y));
}

int DecoderBase::decodeRaw(){
    return input_file.getInt(dataset.bits());
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
