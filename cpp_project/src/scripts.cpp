
#include "scripts.h"

#include <iostream>
#include "coder_basic.h"
#include "decoder_basic.h"
#include "csv_utils.h"
#include "csv_reader.h"
#include "csv_writer.h"
#include "bit_stream_reader.h"
#include "bit_stream_writer.h"
#include "dataset_utils.h"
#include "assert.h"

void Scripts::copyAndCompareCSV(){
    std::string input_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    std::string input_filename = "noaa_spc-wind.csv";
    std::string output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    std::string output_filename = "noaa_spc-wind.copy.csv";

    std::cout << "CopyCSV" << std::endl;
    CSVUtils::CopyCSV(input_path, input_filename, output_path, output_filename);
    std::cout << "CompareCSVLossless" << std::endl;
    CSVUtils::CompareCSVLossless(input_path, input_filename, output_path, output_filename);
}

void Scripts::codeAndDecodeCSV(){
    std::string input_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    std::string input_filename = "noaa_spc-wind.csv";
    std::string coded_filename = "noaa_spc-wind.csv.c";
    std::string decoded_filename = "noaa_spc-wind.csv.c.d";

    CSVReader csv_reader = CSVReader(input_path, input_filename);
    std::string coded_path = input_path + "/" + coded_filename;
    BitStreamWriter bit_stream_writer = BitStreamWriter(coded_path.c_str());

    CoderBasic coder_basic = CoderBasic(csv_reader, bit_stream_writer);
    coder_basic.codeFile();
    coder_basic.close();

    BitStreamReader bit_stream_reader = BitStreamReader(coded_path.c_str());
    std::string decoded_path = input_path + "/" + decoded_filename;
    CSVWriter csv_writer = CSVWriter(input_path, decoded_path);

    DecoderBasic decoder_basic = DecoderBasic(bit_stream_reader, csv_writer);
    decoder_basic.decodeFile();
    decoder_basic.close();
}
