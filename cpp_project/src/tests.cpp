
#include "tests.h"

#include <iostream>
#include "dataset_utils.h"
#include "assert.h"


void Tests::testDatasetUtils(){
    DatasetUtils dataset_utils1 = DatasetUtils("code");
    assert(dataset_utils1.codeDatasetName("SolarAnywhere") == 3);
    assert(dataset_utils1.codeDatasetName("NOAA-SPC-wind") == 7);
    assert(dataset_utils1.codeTimeUnit("seconds") == 0);
    dataset_utils1.close();

    DatasetUtils dataset_utils2 = DatasetUtils("decode");
    assert(dataset_utils2.decodeDatasetName(3) == "SolarAnywhere");
    assert(dataset_utils2.decodeDatasetName(7) == "NOAA-SPC-wind");
    assert(dataset_utils2.decodeTimeUnit(0) == "seconds");
    dataset_utils2.close();

    DatasetUtils dataset_utils = DatasetUtils("code");
    std::vector<Range> range_vector = dataset_utils.getRangeVector("SolarAnywhere");
    std::vector<Range> expected_range_vector = {Range(0,131071), Range(0,1020), Range(0,970), Range(0,800)};
    assert(range_vector.size() == 4);
    for(int i = 0; i < range_vector.size(); i++){
        assert(range_vector[i].begin == expected_range_vector[i].begin);
        assert(range_vector[i].end == expected_range_vector[i].end);
    }

    std::vector<int> bits_vector = dataset_utils.getBitsVector("SolarAnywhere");
    std::vector<int> expected_bits_vector = {17,10,10,10};
    assert(bits_vector == expected_bits_vector);

    dataset_utils.close();
}
