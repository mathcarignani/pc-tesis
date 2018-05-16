
#include "tests.h"

#include <iostream>
#include "dataset_utils.h"
#include "assert.h"
#include "header_utils.h"
#include <math.h>


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

void Tests::testDatetimeUtils(){
    std::cout << "Tests::testDatetimeUtils" << std::endl;

    std::string date_format = "%Y-%m-%d %H:%M:%S";
    std::tm start_date = DatetimeUtils::parseDate("1900-01-01 00:00:00", date_format);
    std::tm end_date = DatetimeUtils::parseDate("2036-02-07 06:28:16", date_format);
    assert(DatetimeUtils::compareDates(start_date, start_date) == 0);
    assert(DatetimeUtils::compareDates(start_date, end_date) == 1);
    assert(DatetimeUtils::compareDates(end_date, start_date) == -1);

    std::tm start_date_plus_1_second = DatetimeUtils::parseDate("1900-01-01 00:00:01", date_format);
    std::tm start_date_plus_50_years = DatetimeUtils::parseDate("1950-01-01 00:00:00", date_format);
    std::tm start_date_plus_100_years = DatetimeUtils::parseDate("2000-01-01 00:00:00", date_format);
    std::tm start_date_plus_110_years = DatetimeUtils::parseDate("2010-01-01 00:00:00", date_format);
    std::tm start_date_plus_120_years = DatetimeUtils::parseDate("2020-01-01 00:00:00", date_format);
    std::tm start_date_plus_136_years = DatetimeUtils::parseDate("2036-01-01 00:00:00", date_format);

    assert(DatetimeUtils::datetimeToSecondsSince(start_date, start_date) == 0);
    assert(DatetimeUtils::datetimeToSecondsSince(start_date, start_date_plus_1_second) == 1);
    assert(DatetimeUtils::datetimeToSecondsSince(start_date, start_date_plus_50_years) == 1577836800);
    assert(DatetimeUtils::datetimeToSecondsSince(start_date, start_date_plus_100_years) == 3155673600);
    assert(DatetimeUtils::datetimeToSecondsSince(start_date, start_date_plus_110_years) == 3471292800);
    assert(DatetimeUtils::datetimeToSecondsSince(start_date, start_date_plus_120_years) == 3786825600);
    assert(DatetimeUtils::datetimeToSecondsSince(start_date, start_date_plus_136_years) == 4291747200);
    assert(DatetimeUtils::datetimeToSecondsSince(start_date, end_date) == pow(2,32));
}