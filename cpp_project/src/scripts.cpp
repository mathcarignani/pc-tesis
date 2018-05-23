
#include "scripts.h"

#include <iostream>
#include "coder_basic.h"
#include "decoder_basic.h"
#include "coder_pca.h"
//#include "decoder_pca.h"
#include "coder_apca.h"
#include "csv_utils.h"
#include "bit_stream_utils.h"
#include "assert.h"


void Scripts::codeBasic(Path input_path, Path output_path){
    CSVReader csv_reader = CSVReader(input_path);
    BitStreamWriter bit_stream_writer = BitStreamWriter(output_path);
    CoderBasic coder = CoderBasic(csv_reader, bit_stream_writer);
    coder.codeFile();
    coder.close();
}

void Scripts::decodeBasic(Path input_path, Path output_path){
    BitStreamReader bit_stream_reader = BitStreamReader(input_path);
    CSVWriter csv_writer = CSVWriter(output_path);
    DecoderBasic decoder = DecoderBasic(bit_stream_reader, csv_writer);
    decoder.decodeFile();
    decoder.close();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void Scripts::codePCA(Path input_path, Path output_path, int fixed_window_size, std::vector<int> error_thresholds_vector){
    CSVReader csv_reader = CSVReader(input_path);
    BitStreamWriter bit_stream_writer = BitStreamWriter(output_path);
    CoderPCA coder = CoderPCA(csv_reader, bit_stream_writer);
    coder.setCoderParams(fixed_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.close();
}

void Scripts::decodePCA(Path input_path, Path output_path, int fixed_window_size, std::vector<int> error_thresholds_vector){

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void Scripts::codeAPCA(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector){
    CSVReader csv_reader = CSVReader(input_path);
    BitStreamWriter bit_stream_writer = BitStreamWriter(output_path);
    CoderAPCA coder = CoderAPCA(csv_reader, bit_stream_writer);
    coder.setCoderParams(max_window_size, error_thresholds_vector);
    coder.codeFile();
    coder.close();
}

void Scripts::decodeAPCA(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector){

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void Scripts::copyAndCompareCSV(){
    std::string project_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    Path input_path = Path(project_path, "noaa_spc-wind.csv");
    Path copy_path = Path(project_path, "noaa_spc-wind.copy.csv");

    std::cout << "CopyCSV" << std::endl;
    CSVUtils::CopyCSV(input_path, copy_path);

    std::cout << "Compare" << std::endl;
    CSVUtils::CompareCSVLossless(input_path, copy_path);

    int first_diff_bit = BitStreamUtils::compare(input_path, copy_path);
    if (first_diff_bit !=0 ) { std::cout << "ERROR: first different bit = " << first_diff_bit << std::endl; }
    assert(first_diff_bit == 0);
}

void Scripts::codeAndDecodeCSV(){
    std::string project_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/cpp_project";
    Path input_path = Path(project_path, "noaa_spc-wind.csv");
    Path coded_path = Path(project_path, "noaa_spc-wind.csv.c");
    Path decoded_path = Path(project_path, "noaa_spc-wind.csv.c.d.csv");

    std::cout << "codeCSV" << std::endl;
    std::vector<int> error_thresholds_vector;
    for(int i=0; i < 11; i++) { error_thresholds_vector.push_back(0); }
    codeAPCA(input_path, coded_path, 5, error_thresholds_vector);


//    std::cout << "codeCSV" << std::endl;
//    codeBasic(input_path, coded_path);
//    std::cout << "decodeCSV" << std::endl;
//    decodeBasic(coded_path, decoded_path);
//
//    std::cout << "Compare" << std::endl;
//    CSVUtils::CompareCSVLossless(input_path, decoded_path);
//
//    int first_diff_bit = BitStreamUtils::compare(input_path, decoded_path);
//    if (first_diff_bit !=0 ) { std::cout << "ERROR: first different bit = " << first_diff_bit << std::endl; }
//    assert(first_diff_bit == 0);
}
