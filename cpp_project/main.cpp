
#include <datetime_utils.h>
#include "scripts.h"
#include "tests.h"
#include "assert.h"
#include "bit_stream_utils.h"
#include "path.h"
#include <stdlib.h>
#include <vector>

int main(int argc, char *argv[]){
    std::cout << "argc " << argc << std::endl;
    for (int i=0; i<argc; i++){
        std::cout << i << " " << argv[i] << std::endl;
    }

    if (argc <= 1){
//    std::string path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/[3]noaa-adcp/basic";
//    assert(BitStreamUtils::compareBytes(path, "noaa-adcp-201501.c.cpp.csv", path, "noaa-adcp-201501.c.python.csv") == 0);
//    Scripts::copyAndCompareCSV();
        Scripts::codeAndDecodeCSV();

//    Tests::testDatasetUtils();
//    Tests::testDatetimeUtils();
//    Tests::testStringUtils();
        return 0;
    }

    // argc > 1
    std::string action = argv[1]; // "c" or "d"
    assert(action == "c" or action == "d");

    Path input_path = Path(argv[2], argv[3]);
    Path output_path = Path(argv[4], argv[5]);

    std::string coder_name = argv[6];
    if (coder_name == "CoderBasic"){
        assert(argc == 7);
        if (action == "c"){   Scripts::codeBasic(input_path, output_path); }
        else              { Scripts::decodeBasic(input_path, output_path); }
    }
    else {
        bool coders1 = coder_name == "CoderPCA" || coder_name == "CoderAPCA" || coder_name == "CoderPWLH";
        bool coders2 = coder_name == "CoderCA" || coder_name == "CoderSF";
        assert(coders1 || coders2);
        assert(argc >= 9);
        int window_size = atoi(argv[7]); // fixed_window_size for PCA and max_window_size for APCA
        std::vector<int> error_thresholds_vector;
        for(int i=8; i < argc; i++){ error_thresholds_vector.push_back(atoi(argv[i])); }

        if (coder_name == "CoderPCA"){
            if (action == "c") {   Scripts::codePCA(input_path, output_path, window_size, error_thresholds_vector); }
            else               { Scripts::decodePCA(input_path, output_path, window_size); }
        }
        else if (coder_name == "CoderPCA"){
            if (action == "c") {   Scripts::codeAPCA(input_path, output_path, window_size, error_thresholds_vector); }
            else               { Scripts::decodeAPCA(input_path, output_path, window_size); }
        }
        else if (coder_name == "CoderPWLH"){
            if (action == "c") {   Scripts::codePWLH(input_path, output_path, window_size, error_thresholds_vector); }
            else               { Scripts::decodePWLH(input_path, output_path, window_size); }
        }
        else if (coder_name == "CoderCA"){
            if (action == "c") {   Scripts::codeCA(input_path, output_path, window_size, error_thresholds_vector); }
            else               { Scripts::decodeCA(input_path, output_path, window_size); }
        }
        else { // coder_name == "CoderSF"
            if (action == "c") {   Scripts::codeSF(input_path, output_path, window_size, error_thresholds_vector); }
            else               { Scripts::decodeSF(input_path, output_path, window_size); }
        }

    }

    return 0;
}
