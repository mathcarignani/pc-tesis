#include <datetime_utils.h>
#include "scripts.h"
#include "tests.h"
#include "tests_coders.h"
#include "assert.h"
#include "string_utils.h"

//
// USAGE - EXAMPLES:
//
// (1) Code with CoderBase (no window_size param, no err params)
// exe_path c input_path input_filename output_path output_filename CoderBase
//
// (2) Code with CoderPCA
// exe_path c input_path input_filename output_path output_filename CoderPCA window_size err1 err2 ... errN
//
// (3) Decode
// exe_path d input_path input_filename output_path output_filename
//
int main(int argc, char *argv[]){
#if !(MASK_MODE >= 0 && MASK_MODE <= 3)
    std::cout << "ERROR: MASK_MODE must be 0, 1, 2, or 3." << std::endl;
    return -1;
#endif //

//    std::cout << "argc " << argc << std::endl;
//    for (int i=0; i<argc; i++){
//        std::cout << i << " " << argv[i] << std::endl;
//    }

    if (argc <= 1) {
        TestsCoders::testSingleCoder();
        Tests::runAll();
        return 0;
    }

    // argc > 1
    std::string action = argv[1];
    assert(action == "c" or action == "d");

    Path input_path = Path(argv[2], argv[3]);
    Path output_path = Path(argv[4], argv[5]);

    if (action == "d"){
        assert(argc == 6);
        Scripts::decode(input_path, output_path);
        return 0;
    }

    // action == "c"
    std::string coder_name = argv[6];
    std::vector<std::string> coders_array{"CoderBase", "CoderPCA", "CoderAPCA", "CoderPWLH",
                                          "CoderPWLHInt", "CoderCA", "CoderSF", "CoderFR",
                                          "CoderGAMPS", "CoderGAMPSLimit"};

    if (coder_name == "CoderBase"){
        assert(argc == 7);
        Scripts::codeBase(input_path, output_path);
        return 0;
    }

    assert(StringUtils::stringInList(coder_name, coders_array));
    assert(argc >= 9);
    int window_size = atoi(argv[7]);
    std::vector<int> error_thresholds_vector;
    for(int i=8; i < argc; i++){ error_thresholds_vector.push_back(atoi(argv[i])); }

    Scripts::code(coder_name, input_path, output_path, window_size, error_thresholds_vector);
    return 0;
}
