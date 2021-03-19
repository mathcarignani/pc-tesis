
#include "scripts.h"

#include <iostream>
#include "decoder_common.h"
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

void Scripts::decode(Path input_path, Path output_path){
    BitStreamReader* bit_stream_reader = new BitStreamReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    DecoderCommon* decoder = DecoderCommon::getDecoder(bit_stream_reader, csv_writer);
    decoder->decodeFile();
    decoder->close();
}

Dataset* Scripts::codeBase(Path input_path, Path output_path){
    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);
    CoderBase* coder = new CoderBase("CoderBase", csv_reader, bit_stream_writer);
    return coder->code();
}

Dataset* Scripts::code(std::string coder_name, Path input_path, Path output_path,
                       int window_size, std::vector<int> error_thresholds_vector){
    if (!StringUtils::find(coder_name, "Coder")){
        coder_name = "Coder" + coder_name;
    }
    Constants::getCoderValue(coder_name); // check if coder_name is valid

    CSVReader* csv_reader = new CSVReader(input_path);
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(output_path);

    CoderCommon* coder;

    if (coder_name == "CoderPCA"){
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
        bool integer_mode = coder_name == "CoderPWLHInt";
        ((CoderPWLH*) coder)->setCoderParams(window_size, error_thresholds_vector, integer_mode);
    }
#if MASK_MODE
    else if (coder_name == "CoderSF"){
        new CoderSlideFilter(coder_name, csv_reader, bit_stream_writer);
        ((CoderSlideFilter*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
    else if (coder_name == "CoderFR"){
        new CoderFR(coder_name, csv_reader, bit_stream_writer);
        ((CoderFR*) coder)->setCoderParams(window_size, error_thresholds_vector);
    }
#endif
    if { // (coder_name == "CoderGAMPS" || coder_name == "CoderGAMPSLimit") {
        new CoderGAMPS(coder_name, csv_reader, bit_stream_writer);
        bool limit_mode = coder_name == "CoderGAMPSLimit";
        ((CoderGAMPS*) coder)->setCoderParams(window_size, error_thresholds_vector, limit_mode);
    }
    return coder->code();
}
