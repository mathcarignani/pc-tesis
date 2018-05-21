
#include <datetime_utils.h>
#include "scripts.h"
#include "tests.h"
#include "assert.h"
#include "bit_stream_utils.h"

int main(int argc, char *argv[]){
    if (argc > 1){
        std::string action = argv[1]; // "c" or "d"
        assert(action == "c" or action == "d");

        std::string input_path = argv[2];
        std::string input_filename = argv[3];
        std::string output_path = argv[4];
        std::string output_filename = argv[5];

        std::cout << "input_path=" << input_path << std::endl;
        std::cout << "input_filename=" << input_filename << std::endl;
        std::cout << "output_path=" << output_path << std::endl;
        std::cout << "output_filename=" << output_filename << std::endl;

        std::string coder_name = argv[6];
        assert(coder_name == "CoderBasic");

        if (action == "c"){
            Scripts::codeCSV(input_path, input_filename, output_path, output_filename);
        }
        else{
            Scripts::decodeCSV(input_path, input_filename, output_path, output_filename);
        }

        return 0;
    }
    std::string path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/[3]noaa-adcp/basic";
    assert(BitStreamUtils::compareBytes(path, "noaa-adcp-201501.c.cpp.csv", path, "noaa-adcp-201501.c.python.csv") == 0);
//    Scripts::copyAndCompareCSV();
//    Scripts::codeAndDecodeCSV();

//    Tests::testDatasetUtils();
//    Tests::testDatetimeUtils();
//    Tests::testStringUtils();
    return 0;
}



