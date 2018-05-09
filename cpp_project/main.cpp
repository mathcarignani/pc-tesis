#include <cstring>
#include <iostream>
#include <stdlib.h>

#include "csv_utils.h"
#include "coder_basic.h"
#include "decoder_basic.h"
#include "bit_stream_reader.h"
#include "bit_stream_writer.h"
#include "csv_reader.h"
#include "csv_writer.h"


//#include "file_utils.h"

int main(int argc, char *argv[]){

//    // COPY AND COMPARE CSV
//    std::string input_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
//    std::string input_filename = "noaa_spc-wind.csv";
//    std::string output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
//    std::string output_filename = "noaa_spc-wind.copy.csv";
//
//    CSVUtils::CopyCSV(input_path, input_filename, output_path, output_filename);
//    CSVUtils::CompareCSVLossless(input_path, input_filename, output_path, output_filename);

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

//    CSVWriter csv_writer = CSVWriter(input_path, decoded_filename);
//    std::string decoded_path = input_path + "/" + coded_filename;
//    DecoderBasic decoder_basic = DecoderBasic(, csv_writer);
//    decoder_basic.decodeFile();
//    decoder_basic.close();

    return 0;
}

//// imprimo entrada al main
//for(int i=0; i<argc; i++){
//std::cout << argv[i] << " ";
//}
//std::cout << std::endl << std::endl;
//
//const std::string filename("elnino-clean.csv");
//const std::string coded_filename("elnino-clean.csv.coded");
//const std::string decoded_filename("elnino-clean.csv.decoded.csv");
//
//std::cout << "Coding csv...\n";
//CsvUtils::code_csv(filename, coded_filename);
//
//std::cout << "Decoding csv...\n";
//CsvUtils::decode_csv(coded_filename, decoded_filename);
//
//std::cout << "Comparing csv...\n";
//// int res = FileUtils::compare((char*)filename.c_str(), (char*)decoded_filename.c_str());
//// int res = CsvUtils::compare_csv(filename, decoded_filename);
//// std::cout << res << "\n";