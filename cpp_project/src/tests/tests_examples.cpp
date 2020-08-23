
#include "tests_examples.h"
//#include "assert.h"
#include "tests_utils.h"
#include "path.h"
#include "scripts.h"
#include "tests_coders_utils.h"
#include "bit_stream_utils.h"

void TestsExamples::runAll(){
    std::cout << "  pcaTest()" << std::endl;  pcaTest();
    std::cout << "  apcaTest()" << std::endl; apcaTest();
}

void TestsExamples::commonTest(std::string input_filename, std::string coder_name,
                               int window_size, std::vector<int> error_thresholds_vector){
    Path input_path = Path(EXAMPLES_PATH, input_filename);
    Path coded_path = TestsCodersUtils::codedFilePath(OUTPUT_PATH, input_path, coder_name);

    Path expected_decoded_path = TestsCodersUtils::decodedFilePath(EXPECTED_PATH, coded_path, coder_name);
#if RECORD_TESTS
    Path decoded_path = expected_decoded_path;
#else
    Path decoded_path = TestsCodersUtils::decodedFilePath(OUTPUT_PATH, coded_path, coder_name);
#endif // RECORD_TESTS

    Scripts::code(coder_name, input_path, coded_path, window_size, error_thresholds_vector);
    Scripts::decode(coded_path, decoded_path);
    BitStreamUtils::removeFile(coded_path);

#if !RECORD_TESTS
    TestsCodersUtils::compareFiles(decoded_path, expected_decoded_path);
    BitStreamUtils::removeFile(decoded_path);
#endif // !RECORD_TESTS
}

void TestsExamples::pcaTest(){
    std::vector<int> vector{0, 1};
    commonTest("example1.csv", "PCA", 4, vector);

};

void TestsExamples::apcaTest(){
    std::vector<int> vector{0, 1};
    commonTest("example1.csv", "APCA", 256, vector);
};

const std::string TestsExamples::EXAMPLES_PATH = TestsUtils::OUTPUT_PATH + "/examples";
const std::string TestsExamples::EXPECTED_PATH = EXAMPLES_PATH + "/expected";
const std::string TestsExamples::OUTPUT_PATH = EXAMPLES_PATH + "/output";

