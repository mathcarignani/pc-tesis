
#include "decoder_base.h"

#include "header_decoder.h"
#include "string_utils.h"

// TODO: move this logic to a separate file
#include "decoder_basic.h"
#include "decoder_pca.h"
#include "decoder_apca.h"
#include "decoder_pwlh.h"
#include "decoder_ca.h"
#include "decoder_fr.h"
#include "decoder_slide_filter.h"
#include "decoder_gamps.h"
#include "math_utils.h"


void DecoderBase::setWindowSize(int window_size_){
    window_size = window_size_;
    window_size_bit_length = MathUtils::bitLength(window_size);
}

DecoderBase* DecoderBase::getDecoder(BitStreamReader* input_file, CSVWriter* output_csv){
    int coder_code = input_file->getInt(8); // 8 bits for the coder_code
    int window_size = input_file->getInt(8); // 8 bits for the window_size

    DecoderBase* decoder;

    if (coder_code == 0) {
        decoder = new DecoderBasic(input_file, output_csv);
        return decoder;
    }

    if (coder_code == 10){
        decoder = new DecoderPCA(input_file, output_csv);
    }
    else if (coder_code == 11){
        decoder = new DecoderAPCA(input_file, output_csv);
    }
    else if (coder_code == 20 || coder_code == 21){
        decoder = new DecoderPWLH(input_file, output_csv);
        bool integer_mode = coder_code == 21;
        ((DecoderPWLH*) decoder)->setIntegerMode(integer_mode);
    }
    else if (coder_code == 22){
        decoder = new DecoderCA(input_file, output_csv);
    }
#if MASK_MODE
    else if (coder_code == 23){
        decoder = new DecoderFR(input_file, output_csv);
    }
    else if (coder_code == 24){
        decoder = new DecoderSlideFilter(input_file, output_csv);
    }
#endif
    else if (coder_code == 30){
        decoder = new DecoderGAMPS(input_file, output_csv);
    }
    decoder->setWindowSize(window_size);
    return decoder;
}

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

int DecoderBase::decodeUnary(){
    int value = 0;
    while (!decodeBool()) { value++; }
    return value;
}

std::string DecoderBase::decodeValueRaw(){
    int value = decodeRaw();
    std::string coded_value;
    try {
        coded_value = decodeValue(value);
    }
    catch( const std::invalid_argument& e ){
        std::cout << "DecoderBase::decodeValueRaw: " << e.what() << std::endl;
        exit(-1);
    }
    return coded_value;
}

float DecoderBase::decodeFloat(){
    return input_file->getFloat();
}

double DecoderBase::decodeDouble(){
    return input_file->getDouble();
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
