#include <cstring>
#include <iostream>
#include <stdlib.h>

#include "csv_utils.h"
//#include "file_utils.h"

int main(int argc, char *argv[]){

    std::string input_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    std::string input_filename = "noaa_spc-wind.csv";
    std::string output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    std::string output_filename = "noaa_spc-wind.copy.csv";

    CSVUtils::CopyCSV(input_path, input_filename, output_path, output_filename);
    CSVUtils::CompareCSV(input_path, input_filename, output_path, output_filename);

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