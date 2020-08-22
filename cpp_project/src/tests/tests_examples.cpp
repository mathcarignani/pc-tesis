
#include "tests_examples.h"
//#include "assert.h"
#include "tests_utils.h"
#include "path.h"
#include "scripts.h"

void TestsExamples::runAll(){
    std::cout << "  pcaTest()" << std::endl; pcaTest();
}

void TestsExamples::pcaTest(){
    Path input_path = Path(EXAMPLES_PATH, "example1.csv");
    Path coded_path = Path(OUTPUT_PATH, "example1-pca.csv");
    Path decoded_path = Path(OUTPUT_PATH, "example1-pca-deco.csv");
    std::vector<int> pca_vector{0, 1};
    Scripts::code("CoderPCA", input_path, coded_path, 4, pca_vector);
    Scripts::decode(coded_path, decoded_path);
};

const std::string TestsExamples::EXAMPLES_PATH = TestsUtils::OUTPUT_PATH + "/examples";
const std::string TestsExamples::EXPECTED_PATH = EXAMPLES_PATH + "/expected";
const std::string TestsExamples::OUTPUT_PATH = EXAMPLES_PATH + "/output";
