
#include "tests_examples.h"
//#include "assert.h"
#include "tests_utils.h"
#include "path.h"
#include "scripts.h"
#include "tests_coders_utils.h"
#include "bit_stream_utils.h"

void TestsExamples::runAll(){
    std::vector<int> vector_pca{0, 1};
    commonTest("example1.csv", "PCA", 4, vector_pca);

    std::vector<int> vector_apca{0, 1};
    commonTest("example1.csv", "APCA", 256, vector_apca);

    std::vector<int> vector_ca{0, 1};
    commonTest("example1.csv", "CA", 256, vector_ca);

    std::vector<int> vector_pwlh{0, 1};
    commonTest("example1.csv", "PWLH", 256, vector_pwlh);

    std::vector<int> vector_pwlhint{0, 1};
    commonTest("example1.csv", "PWLHInt", 256, vector_pwlhint);

    std::vector<int> vector_sf{0, 1};
    commonTest("example1.csv", "SF", 256, vector_sf);

    std::vector<int> vector_fr{0, 1};
    commonTest("example1.csv", "FR", 256, vector_fr);
}

void TestsExamples::commonTest(std::string input_filename, std::string coder_name,
                               int window_size, std::vector<int> error_thresholds_vector){
    std::cout << "  commonTest(.." + coder_name + ")";
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

const std::string TestsExamples::EXAMPLES_PATH = TestsUtils::OUTPUT_PATH + "/examples";
const std::string TestsExamples::EXPECTED_PATH = EXAMPLES_PATH + "/expected";
const std::string TestsExamples::OUTPUT_PATH = EXAMPLES_PATH + "/output";

