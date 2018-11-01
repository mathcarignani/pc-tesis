
#include "tests_dataset_utils.h"
#include "assert.h"

void TestsDatasetUtils::runAll(){
    std::cout << "  codeTest()" << std::endl;   codeTest();
    std::cout << "  decodeTest()" << std::endl; decodeTest();
    std::cout << "  rangesTest()" << std::endl; rangesTest();
}

void TestsDatasetUtils::codeTest(){
    DatasetUtils dataset_utils = DatasetUtils("code");
    assert(dataset_utils.codeDatasetName("SolarAnywhere") == 3);
    assert(dataset_utils.codeDatasetName("NOAA-SPC-wind") == 7);
    assert(dataset_utils.codeTimeUnit("seconds") == 0);
    dataset_utils.close();
}

void TestsDatasetUtils::decodeTest(){
    DatasetUtils dataset_utils = DatasetUtils("decode");
    assert(dataset_utils.decodeDatasetName(3) == "SolarAnywhere");
    assert(dataset_utils.decodeDatasetName(7) == "NOAA-SPC-wind");
    assert(dataset_utils.decodeTimeUnit(0) == "seconds");
    dataset_utils.close();
}

void TestsDatasetUtils::rangesTest(){
    DatasetUtils dataset_utils = DatasetUtils("code");
    std::vector<Range> range_vector = dataset_utils.getRangeVector("SolarAnywhere");
    std::vector<Range> expected_range_vector = {Range(0,131071), Range(0,1020), Range(0,970), Range(0,800)};
    assert(range_vector.size() == 4);
    for(int i = 0; i < range_vector.size(); i++){
        assert(range_vector[i].begin == expected_range_vector[i].begin);
        assert(range_vector[i].end == expected_range_vector[i].end);
    }
    dataset_utils.close();
}
