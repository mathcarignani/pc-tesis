
#include "scripts.h"

#include <iostream>
#include "coder_basic.h"
#include "decoder_basic.h"
#include "coder_pca.h"
#include "decoder_pca.h"
#include "coder_apca.h"
#include "decoder_apca.h"
#include "coder_pwlh.h"
#include "decoder_pwlh.h"
#include "coder_ca.h"
#include "decoder_ca.h"
#include "coder_slide_filter.h"
#include "decoder_slide_filter.h"
#include "coder_fr.h"
#include "decoder_fr.h"
#include "coder_gamps.h"
#include "csv_utils.h"
#include "bit_stream_utils.h"
#include "assert.h"


Dataset* Scripts::codeBasic(Path input_path, Path output_path){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderBasic coder = CoderBasic(csv_reader, bit_stream_writer);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodeBasic(Path input_path, Path output_path){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderBasic decoder = DecoderBasic(bit_stream_reader, csv_writer);
    decoder.decodeFile();
    decoder.close();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Dataset* Scripts::codePCA(Path input_path, Path output_path, int fixed_window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderPCA coder = CoderPCA(csv_reader, bit_stream_writer);
    coder.setCoderParams(fixed_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodePCA(Path input_path, Path output_path, int fixed_window_size){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderPCA decoder = DecoderPCA(bit_stream_reader, csv_writer);
    decoder.setCoderParams(fixed_window_size);
    decoder.decodeFile();
    decoder.close();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Dataset* Scripts::codeAPCA(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderAPCA coder = CoderAPCA(csv_reader, bit_stream_writer);
    coder.setCoderParams(max_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodeAPCA(Path input_path, Path output_path, int max_window_size){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderAPCA decoder = DecoderAPCA(bit_stream_reader, csv_writer);
    decoder.setCoderParams(max_window_size);
    decoder.decodeFile();
    decoder.close();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Dataset* Scripts::codePWLH(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector, bool integer_mode){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderPWLH coder = CoderPWLH(csv_reader, bit_stream_writer);
    coder.setCoderParams(max_window_size, error_thresholds_vector, integer_mode);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodePWLH(Path input_path, Path output_path, int max_window_size, bool integer_mode){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderPWLH decoder = DecoderPWLH(bit_stream_reader, csv_writer);
    decoder.setCoderParams(max_window_size, integer_mode);
    decoder.decodeFile();
    decoder.close();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Dataset* Scripts::codeCA(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderCA coder = CoderCA(csv_reader, bit_stream_writer);
    coder.setCoderParams(max_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodeCA(Path input_path, Path output_path, int max_window_size){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderCA decoder = DecoderCA(bit_stream_reader, csv_writer);
    decoder.setCoderParams(max_window_size);
    decoder.decodeFile();
    decoder.close();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#if MASK_MODE
Dataset* Scripts::codeSF(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderSlideFilter coder = CoderSlideFilter(csv_reader, bit_stream_writer);
    coder.setCoderParams(max_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodeSF(Path input_path, Path output_path, int max_window_size){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderSlideFilter decoder = DecoderSlideFilter(bit_stream_reader, csv_writer);
    decoder.setCoderParams(max_window_size);
    decoder.decodeFile();
    decoder.close();
}
#endif

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#if MASK_MODE
Dataset* Scripts::codeFR(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderFR coder = CoderFR(csv_reader, bit_stream_writer);
    coder.setCoderParams(max_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodeFR(Path input_path, Path output_path, int max_window_size){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderFR decoder = DecoderFR(bit_stream_reader, csv_writer);
    decoder.setCoderParams(max_window_size);
    decoder.decodeFile();
    decoder.close();
}

Dataset* Scripts::codeGAMPS(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderGAMPS coder = CoderGAMPS(csv_reader, bit_stream_writer);
    coder.setCoderParams(max_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.printBits();
    coder.close();
    return coder.dataset;
}

void Scripts::decodeGAMPS(Path input_path, Path output_path, int max_window_size){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderFR decoder = DecoderFR(bit_stream_reader, csv_writer);
    // DecoderGAMPS decoder = DecoderGAMPS(bit_stream_reader, csv_writer);
    decoder.setCoderParams(max_window_size);
    decoder.decodeFile();
    decoder.close();
}
#endif
