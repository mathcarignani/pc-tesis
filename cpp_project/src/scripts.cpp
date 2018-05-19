
#include "scripts.h"

#include <iostream>
#include "coder_basic.h"
#include "decoder_basic.h"
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
//    std::string input_filename = "noaa_spc-wind.csv";
//    std::string coded_filename = "noaa_spc-wind.csv.c";
//    std::string decoded_filename = "output.csv";

    std::string input_filename = "test.csv";
    std::string coded_filename = "test.csv.c";
    std::string decoded_filename = "test.csv.c.d.csv";

    CSVReader csv_reader = CSVReader(path, input_filename, false);
    std::string coded_path = path + "/" + coded_filename;
    BitStreamWriter bit_stream_writer = BitStreamWriter(coded_path.c_str());

    CoderBasic coder_basic = CoderBasic(csv_reader, bit_stream_writer);
    coder_basic.codeFile();
    coder_basic.close();

    BitStreamReader bit_stream_reader = BitStreamReader(coded_path.c_str());
    CSVWriter csv_writer = CSVWriter(path, decoded_filename);

    DecoderBasic decoder_basic = DecoderBasic(bit_stream_reader, csv_writer);
    decoder_basic.decodeFile();
    decoder_basic.close();

    std::cout << "Compare" << std::endl;
    CSVUtils::CompareCSVLossless(path, input_filename, path, decoded_filename);

    int first_diff_bit = BitStreamUtils::compare(path, input_filename, path, decoded_filename);
    if (first_diff_bit !=0 ) { std::cout << "ERROR: first different bit = " << first_diff_bit << std::endl; }
    assert(first_diff_bit == 0);
}
