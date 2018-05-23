
#include <datetime_utils.h>
#include "scripts.h"
#include "tests.h"
#include "assert.h"
#include "bit_stream_utils.h"
#include "path.h"
#include <stdlib.h>
#include <vector>

int main(int argc, char *argv[]){
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
    else if (coder_name == "CoderPCA"){
        assert(argc >= 9);
        int fixed_window_size = atoi(argv[7]);
        std::vector<int> error_thresholds_vector;
        for(int i=8; i < argc; i++){
            int error_threshold = atoi(argv[i]);
            error_thresholds_vector.push_back(error_threshold);
        }

        if (action == "c") {   Scripts::codePCA(input_path, output_path, fixed_window_size, error_thresholds_vector); }
        else               { Scripts::decodePCA(input_path, output_path, fixed_window_size, error_thresholds_vector); }
    }

    return 0;
}
