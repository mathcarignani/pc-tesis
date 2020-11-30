
#include "decoder_common.h"

#include "header_decoder.h"
#include "conversor.h"

// TODO: move this logic to a separate file
#include "decoder_base.h"
#include "decoder_pca.h"
#include "decoder_apca.h"
#include "decoder_pwlh.h"
#include "decoder_ca.h"
#include "decoder_fr.h"
#include "decoder_slide_filter.h"
#include "decoder_gamps.h"
#include "math_utils.h"


void DecoderCommon::setWindowSize(int window_size_){
    window_size = window_size_;
    window_size_bit_length = MathUtils::windowSizeBitLength(window_size);
}

DecoderCommon* DecoderCommon::getDecoder(BitStreamReader* input_file, CSVWriter* output_csv){
    int coder_code = input_file->getInt(8); // 8 bits for the coder_code
    int window_size = input_file->getInt(8) + 1; // 8 bits for the window_size

    DecoderCommon* decoder;

    if (coder_code == Constants::CODER_BASE) {
        decoder = new DecoderBase(input_file, output_csv);
        return decoder;
    }

    if (coder_code == Constants::CODER_PCA){
        decoder = new DecoderPCA(input_file, output_csv);
    }
    else if (coder_code == Constants::CODER_APCA){
        decoder = new DecoderAPCA(input_file, output_csv);
    }
    else if (coder_code == Constants::CODER_PWLH || coder_code == Constants::CODER_PWLH_INT){
        decoder = new DecoderPWLH(input_file, output_csv);
        bool integer_mode = coder_code == Constants::CODER_PWLH_INT;
        ((DecoderPWLH*) decoder)->setIntegerMode(integer_mode);
    }
    else if (coder_code == Constants::CODER_CA){
        decoder = new DecoderCA(input_file, output_csv);
    }
#if MASK_MODE
    else if (coder_code == Constants::CODER_FR){
        decoder = new DecoderFR(input_file, output_csv);
    }
    else if (coder_code == Constants::CODER_SF){
        decoder = new DecoderSlideFilter(input_file, output_csv);
    }
#endif
    else if (coder_code == Constants::CODER_GAMPS || coder_code == Constants::CODER_GAMPS_LIMIT){
        decoder = new DecoderGAMPS(input_file, output_csv);
        bool limit_mode = coder_code == Constants::CODER_GAMPS_LIMIT;
        ((DecoderGAMPS*) decoder)->setLimitMode(limit_mode);
    }
    decoder->setWindowSize(window_size);
    return decoder;
}

DecoderCommon::DecoderCommon(BitStreamReader* input_file_, CSVWriter* output_csv_){
    input_file = input_file_;
    output_csv = output_csv_;
}

void DecoderCommon::decodeDataRowsCount(){
    data_rows_count = input_file->getInt(24); // 24 bits for the data rows count
}

std::string DecoderCommon::decodeValue(int y){
    if (y == dataset->nan()) { return Constants::NO_DATA; }

    y -= dataset->offset();
    if (dataset->insideRange(y)) { return Conversor::intToString(y); }

    throw std::invalid_argument(Conversor::intToString(y));
}

int DecoderCommon::decodeRaw(){
    return input_file->getInt(dataset->bits());
}

bool DecoderCommon::decodeBool(){
    if (input_file->getBit()) { return true; } else { return false; }
}

int DecoderCommon::decodeInt(int bits){
    return (input_file->getInt(bits));
}

int DecoderCommon::decodeWindowLength(int window_size_bit_length){
    return input_file->getInt(window_size_bit_length) + 1;
}

int DecoderCommon::decodeWindowLength(){
    return decodeWindowLength(window_size_bit_length);
}

int DecoderCommon::decodeUnary(){
    int value = 0;
    while (!decodeBool()) { value++; }
    return value;
}

std::string DecoderCommon::decodeValueRaw(){
    int value = decodeRaw();
    std::string coded_value;
    try {
        coded_value = decodeValue(value);
        // std::cout << "decodeValue(" << value << ") = " << coded_value << std::endl;
    }
    catch( const std::invalid_argument& e ){
        std::cout << "DecoderCommon::decodeValueRaw: " << e.what() << std::endl;
        delete input_file;
        delete output_csv;
        exit(-1);
    }
    return coded_value;
}

float DecoderCommon::decodeFloat(){
    return input_file->getFloat();
}

double DecoderCommon::decodeDouble(){
    return input_file->getDouble();
}

void DecoderCommon::flushByte(){
    input_file->flushByte();
}

void DecoderCommon::decodeFile(){
    dataset = HeaderDecoder(input_file, output_csv).decodeHeader();
    decodeDataRowsCount();
    decodeDataRows();
}

void DecoderCommon::close(){
    delete input_file;
    delete output_csv;
}

void DecoderCommon::transposeMatrix(int data_rows_count_, std::vector<std::vector<std::string>> columns, int total_columns){
    for(int row_index_ = 0; row_index_ < data_rows_count_; row_index_++){
        std::vector<std::string> row;
        for(int column_index_ = 0; column_index_ < total_columns; column_index_++) {
            row.push_back(columns[column_index_][row_index_]);
        }
        output_csv->writeRowDecoder(row);
    }
}
