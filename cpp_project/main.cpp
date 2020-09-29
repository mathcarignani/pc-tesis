#include <datetime_utils.h>
#include "scripts.h"
#include "tests.h"
#include "tests_coders.h"
#include "assert.h"
#include "string_utils.h"

//
// USAGE - EXAMPLES:
//
// (1) MASK_MODE == 0, Code with CoderBase (no window_size param, no err params)
// exe_path 0 c input_path output_path CoderBase
//
// (2) MASK_MODE == 3, Code with CoderPCA
// exe_path 3 c input_path output_path CoderPCA window_size err1 err2 ... errN
//
// (3) MASK_MODE == 0, Decode
// exe_path 0 d input_path output_path
//
int main(int argc, char *argv[]){
    assert(Constants::validMaskMode());

//    std::cout << "argc " << argc << std::endl;
//    for (int i=0; i<argc; i++){
//        std::cout << i << " " << argv[i] << std::endl;
//    }

    if (argc <= 1) {
//        TestsCoders::testSingleCoder();
        Tests::runAll();
        return 0;
    }

    // argc > 1
    std::string mask_mode = argv[1];
    assert(Constants::checkMaskMode(mask_mode));

    std::string action = argv[2];
    assert(action == "c" or action == "d");

    Path input_path = Path(argv[3]);
    Path output_path = Path(argv[4]);

    if (action == "d"){
        assert(argc == 5);
        Scripts::decode(input_path, output_path);
        return 0;
    }

    // action == "c"
    std::string coder_name = argv[5];
    std::vector<std::string> coders_array{"CoderBase", "CoderPCA", "CoderAPCA", "CoderPWLH",
                                          "CoderPWLHInt", "CoderCA", "CoderSF", "CoderFR",
                                          "CoderGAMPS", "CoderGAMPSLimit"};

    if (coder_name == "CoderBase"){
        assert(argc == 6);
        Scripts::codeBase(input_path, output_path);
        return 0;
    }

    assert(StringUtils::stringInList(coder_name, coders_array));
    assert(argc >= 8);
    int window_size = atoi(argv[6]);
    std::vector<int> error_thresholds_vector;
    for(int i=7; i < argc; i++){ error_thresholds_vector.push_back(atoi(argv[i])); }

    Scripts::code(coder_name, input_path, output_path, window_size, error_thresholds_vector);
    return 0;
}
