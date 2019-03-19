
#include "tests.h"

#include "tests_string_utils.h"
#include "tests_coders.h"
#include "tests_math_utils.h"
#include "tests_vector_utils.h"
#include "tests_line.h"
#include "tests_header_coder.h"
#include "tests_utils.h"
#include "tests_bit_stream.h"
#include "tests_dataset_utils.h"
#include "tests_datetime_utils.h"
#include "tests_modelKT.h"

void Tests::runAll() {
    std::cout << "TestsMathUtils::runAll();" << std::endl;     TestsMathUtils::runAll();
    std::cout << "TestsStringUtils::runAll();" << std::endl;   TestsStringUtils::runAll();
    std::cout << "TestsVectorUtils::runAll();" << std::endl;   TestsVectorUtils::runAll();
    std::cout << "TestsDatetimeUtils::runAll();" << std::endl; TestsDatetimeUtils::runAll();
    std::cout << "TestsLine::runAll();" << std::endl;          TestsLine::runAll();
    std::cout << "TestsDatasetUtils::runAll();" << std::endl;  TestsDatasetUtils::runAll();
    std::cout << "TestsBitStream::runAll();" << std::endl;     TestsBitStream::runAll();
    std::cout << "TestsHeaderCoder().runAll();" << std::endl;  TestsHeaderCoder().runAll();
    std::cout << "TestsModelKT().runAll();" << std::endl;      TestsModelKT().runAll();
    std::cout << "TestsCoders().runAll();" << std::endl;       TestsCoders().runAll();
}
