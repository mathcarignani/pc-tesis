
#include "scripts.h"

#include <iostream>
#include "decoder_base.h"
#include "coder_basic.h"
#include "coder_pca.h"
#include "coder_apca.h"
#include "coder_pwlh.h"
#include "coder_ca.h"
#include "coder_slide_filter.h"
#include "coder_fr.h"
#include "coder_gamps.h"
#include "csv_utils.h"
#include "bit_stream_utils.h"
#include "assert.h"

void Scripts::decode(Path input_path, Path output_path){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderBase* decoder = DecoderBase::getDecoder(bit_stream_reader, csv_writer);
    decoder->decodeFile();
    decoder->close();
}

Dataset* Scripts::codeBasic(Path input_path, Path output_path){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderBasic* coder = new CoderBasic(csv_reader, bit_stream_writer);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}

Dataset* Scripts::codeOther(std::string coder_name, Path input_path, Path output_path,
                            int window_size, std::vector<int> error_thresholds_vector){
    if (coder_name == "CoderPCA"){
        return Scripts::codePCA(input_path, output_path, window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderAPCA"){
        return Scripts::codeAPCA(input_path, output_path, window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderPWLH" || coder_name == "CoderPWLHint"){
        bool integer_mode = coder_name == "CoderPWLHint";
        return Scripts::codePWLH(input_path, output_path, window_size, error_thresholds_vector, integer_mode);
    }
    else if (coder_name == "CoderCA"){
        return Scripts::codeCA(input_path, output_path, window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderGAMPS"){
        return Scripts::codeGAMPS(input_path, output_path, window_size, error_thresholds_vector);
    }
#if MASK_MODE
    else if (coder_name == "CoderSF"){
        return Scripts::codeSF(input_path, output_path, window_size, error_thresholds_vector);
    }
    else { // if (coder_name == "CoderFR"){
        return Scripts::codeFR(input_path, output_path, window_size, error_thresholds_vector);
    }
#endif
}

Dataset* Scripts::codePCA(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderPCA* coder = new CoderPCA(csv_reader, bit_stream_writer);
    coder->setCoderParams(window_size, error_thresholds_vector);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}

Dataset* Scripts::codeAPCA(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderAPCA* coder = new CoderAPCA(csv_reader, bit_stream_writer);
    coder->setCoderParams(window_size, error_thresholds_vector);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}

Dataset* Scripts::codePWLH(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector, bool integer_mode){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderPWLH* coder = new CoderPWLH(csv_reader, bit_stream_writer);
    coder->setCoderParams(window_size, error_thresholds_vector, integer_mode);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}

Dataset* Scripts::codeCA(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderCA* coder = new CoderCA(csv_reader, bit_stream_writer);
    coder->setCoderParams(window_size, error_thresholds_vector);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}

#if MASK_MODE
Dataset* Scripts::codeSF(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderSlideFilter* coder = new CoderSlideFilter(csv_reader, bit_stream_writer);
    coder->setCoderParams(window_size, error_thresholds_vector);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}

Dataset* Scripts::codeFR(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderFR* coder = new CoderFR(csv_reader, bit_stream_writer);
    coder->setCoderParams(window_size, error_thresholds_vector);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}
#endif

Dataset* Scripts::codeGAMPS(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderGAMPS* coder = new CoderGAMPS(csv_reader, bit_stream_writer);
    coder->setCoderParams(window_size, error_thresholds_vector);
    coder->codeFile();
    coder->printBits();
    coder->close();
    return coder->dataset;
}
