
#include "scripts.h"

#include <iostream>
#include "coder_basic.h"
#include "decoder_basic.h"
#include "coder_pca.h"
//#include "decoder_pca.h"
#include "csv_utils.h"
#include "bit_stream_utils.h"
#include "assert.h"

void Scripts::copyAndCompareCSV(){
    std::string path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    std::string input_filename = "noaa_spc-wind.csv";
    std::string output_filename = "noaa_spc-wind.copy.csv";

    std::cout << "CopyCSV" << std::endl;
    CSVUtils::CopyCSV(path, input_filename, path, output_filename);

    std::cout << "Compare" << std::endl;
    CSVUtils::CompareCSVLossless(path, input_filename, path, output_filename);

    int first_diff_bit = BitStreamUtils::compare(path, input_filename, path, output_filename);
    if (first_diff_bit !=0 ) { std::cout << "ERROR: first different bit = " << first_diff_bit << std::endl; }
    assert(first_diff_bit == 0);
}

void Scripts::codeAndDecodeCSV(){
    std::string path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    std::string input_filename = "noaa_spc-wind.csv";
    std::string coded_filename = "noaa_spc-wind.csv.c";
    std::string decoded_filename = "noaa_spc-wind.csv.c.d.csv";

    std::cout << "codeCSV" << std::endl;
    codeCSV(path, input_filename, path, coded_filename);
    std::cout << "decodeCSV" << std::endl;
    decodeCSV(path, coded_filename, path, decoded_filename);

    std::cout << "Compare" << std::endl;
    CSVUtils::CompareCSVLossless(path, input_filename, path, decoded_filename);

    int first_diff_bit = BitStreamUtils::compare(path, input_filename, path, decoded_filename);
    if (first_diff_bit !=0 ) { std::cout << "ERROR: first different bit = " << first_diff_bit << std::endl; }
    assert(first_diff_bit == 0);
}

void Scripts::codeCSV(std::string input_path, std::string input_filename, std::string output_path, std::string output_filename){
    CSVReader csv_reader = CSVReader(input_path, input_filename);
    std::string coded_path = output_path + "/" + output_filename;
    BitStreamWriter bit_stream_writer = BitStreamWriter(coded_path.c_str());

    // CoderBasic coder = CoderBasic(csv_reader, bit_stream_writer);
    CoderPCA coder = CoderPCA(csv_reader, bit_stream_writer);
    coder.codeFile();
    coder.close();
}

void Scripts::decodeCSV(std::string input_path, std::string input_filename, std::string output_path, std::string output_filename){
    std::string coded_path = input_path + "/" + input_filename;
    BitStreamReader bit_stream_reader = BitStreamReader(coded_path.c_str());
    CSVWriter csv_writer = CSVWriter(output_path, output_filename);

    DecoderBasic decoder = DecoderBasic(bit_stream_reader, csv_writer);
    decoder.decodeFile();
    decoder.close();
}