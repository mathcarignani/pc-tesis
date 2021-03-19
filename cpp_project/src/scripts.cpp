
#include "scripts.h"

#include <iostream>
#include "decoder_base.h"
#include "decoder_pca.h"
#include "decoder_apca.h"
#include "decoder_pwlh.h"
#include "decoder_ca.h"
#include "decoder_slide_filter.h"
#include "decoder_fr.h"
#include "decoder_gamps.h"
#include "coder_base.h"
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
#include "string_utils.h"

Dataset* Scripts::code(std::string coder_name, Path input_path, Path output_path,
                       int window_size, std::vector<int> error_thresholds_vector){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);

    CoderCommon* coder;

    if (coder_name == "CoderBase"){
        coder = new CoderBase(coder_name, csv_reader, bit_stream_writer);
    }
    else if (coder_name == "CoderPCA"){
        coder = new CoderPCA(coder_name, csv_reader, bit_stream_writer);
        ((CoderPCA*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderAPCA"){
        coder = new CoderAPCA(coder_name, csv_reader, bit_stream_writer);
        ((CoderAPCA*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderCA"){
        coder = new CoderCA(coder_name, csv_reader, bit_stream_writer);
        ((CoderCA*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderPWLH" || coder_name == "CoderPWLHInt"){
        coder = new CoderPWLH(coder_name, csv_reader, bit_stream_writer);
        ((CoderPWLH*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
#if MASK_MODE
    else if (coder_name == "CoderSF"){
        coder = new CoderSlideFilter(coder_name, csv_reader, bit_stream_writer);
        ((CoderSlideFilter*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderFR"){
        coder = new CoderFR(coder_name, csv_reader, bit_stream_writer);
        ((CoderFR*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
#endif
    else { // (coder_name == "CoderGAMPS" || coder_name == "CoderGAMPSLimit") {
        coder = new CoderGAMPS(coder_name, csv_reader, bit_stream_writer);
        ((CoderGAMPS*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }

    coder->codeCoderName();
    if (coder_name != "CoderBase") {
        coder->codeWindowParameter();
    }
    return coder->code();
}

void Scripts::decode(Path input_path, Path output_path){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderCommon* decoder;

    std::string coder_name = DecoderCommon::decodeCoderName(bit_stream_reader);

    if (coder_name == "CoderBase") {
        decoder = new DecoderBase(coder_name, bit_stream_reader, csv_writer);
    }
    else {
        if (coder_name == "CoderPCA") {
            decoder = new DecoderPCA(coder_name, bit_stream_reader, csv_writer);
        }
        else if (coder_name == "CoderAPCA") {
            decoder = new DecoderAPCA(coder_name, bit_stream_reader, csv_writer);
        }
        else if (coder_name == "CoderPWLH" || coder_name == "CoderPWLHInt") {
            decoder = new DecoderPWLH(coder_name, bit_stream_reader, csv_writer);
            ((DecoderPWLH *) decoder)->setIntegerMode();
        }
        else if (coder_name == "CoderCA") {
            decoder = new DecoderCA(coder_name, bit_stream_reader, csv_writer);
        }
#if MASK_MODE
        else if (coder_name == "CoderFR") {
            decoder = new DecoderFR(coder_name, bit_stream_reader, csv_writer);
        }
        else if (coder_name == "CoderSF") {
            decoder = new DecoderSlideFilter(coder_name, bit_stream_reader, csv_writer);
        }
#endif
        else { // if (coder_name == "CoderGAMPS" || coder_name == "CoderGAMPSLimit"){
            decoder = new DecoderGAMPS(coder_name, bit_stream_reader, csv_writer);
            ((DecoderGAMPS *) decoder)->setLimitMode();
        }
        decoder->decodeWindowParameter();
    }
    decoder->decode();
}
