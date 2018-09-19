
#include "tests.h"

#include <iostream>
#include "dataset_utils.h"
#include "assert.h"
#include "coders/header/header_utils.h"
#include <math.h>
#include "string_utils.h"
#include "bit_stream_writer.h"
#include "bit_stream_reader.h"
#include <cfloat>
#include <tests_string_utils.h>
#include "tests_coder.h"
#include "tests_math_utils.h"

void Tests::runAll() {
    testDatasetUtils();
    testDatetimeUtils();
    testFloatCoder();
    TestsMathUtils::runAll();
    TestsStringUtils::runAll();
    TestsCoder::testCoderDecoder();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void Tests::testDatasetUtils(){
    std::cout << "Tests::testStringUtils" << std::endl;
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
    std::string start_date_str = "1900-01-01 00:00:00";
    std::string end_date_str = "2036-02-07 06:28:16";

    std::tm start_date = DatetimeUtils::stringToDatetime(start_date_str, date_format);
    std::tm end_date = DatetimeUtils::stringToDatetime(end_date_str, date_format);

    assert(DatetimeUtils::datetimeToString(start_date, date_format) == start_date_str);
    assert(DatetimeUtils::datetimeToString(end_date, date_format) == end_date_str);

    assert(DatetimeUtils::compareDates(start_date, start_date) == 0);
    assert(DatetimeUtils::compareDates(start_date, end_date) == 1);
    assert(DatetimeUtils::compareDates(end_date, start_date) == -1);

    std::tm start_date_plus_1_second = DatetimeUtils::stringToDatetime("1900-01-01 00:00:01", date_format);
    std::tm start_date_plus_50_years = DatetimeUtils::stringToDatetime("1950-01-01 00:00:00", date_format);
    std::tm start_date_plus_100_years = DatetimeUtils::stringToDatetime("2000-01-01 00:00:00", date_format);
    std::tm start_date_plus_110_years = DatetimeUtils::stringToDatetime("2010-01-01 00:00:00", date_format);
    std::tm start_date_plus_120_years = DatetimeUtils::stringToDatetime("2020-01-01 00:00:00", date_format);
    std::tm start_date_plus_136_years = DatetimeUtils::stringToDatetime("2036-01-01 00:00:00", date_format);
    std::tm example_date = DatetimeUtils::stringToDatetime("2015-01-03 09:15:00", date_format);

    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, start_date) == 0);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, start_date_plus_1_second) == 1);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, start_date_plus_50_years) == 1577836800);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, start_date_plus_100_years) == 3155673600);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, start_date_plus_110_years) == 3471292800);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, start_date_plus_120_years) == 3786825600);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, start_date_plus_136_years) == 4291747200);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, example_date) == 3629265300);
    assert(DatetimeUtils::mapDatetimeToSeconds(start_date, end_date) == pow(2,32));

    assert(DatetimeUtils::compareDates(start_date, DatetimeUtils::mapSecondsToDatetime(start_date, 0)) == 0);
    assert(DatetimeUtils::compareDates(start_date_plus_1_second, DatetimeUtils::mapSecondsToDatetime(start_date, 1)) == 0);
    assert(DatetimeUtils::compareDates(start_date_plus_50_years, DatetimeUtils::mapSecondsToDatetime(start_date, 1577836800)) == 0);
    assert(DatetimeUtils::compareDates(start_date_plus_100_years, DatetimeUtils::mapSecondsToDatetime(start_date, 3155673600)) == 0);
    assert(DatetimeUtils::compareDates(start_date_plus_110_years, DatetimeUtils::mapSecondsToDatetime(start_date, 3471292800)) == 0);
    assert(DatetimeUtils::compareDates(start_date_plus_120_years, DatetimeUtils::mapSecondsToDatetime(start_date, 3786825600)) == 0);
    assert(DatetimeUtils::compareDates(start_date_plus_136_years, DatetimeUtils::mapSecondsToDatetime(start_date, 4291747200)) == 0);
    assert(DatetimeUtils::compareDates(example_date, DatetimeUtils::mapSecondsToDatetime(start_date, 3629265300)) == 0);
    assert(DatetimeUtils::compareDates(end_date, DatetimeUtils::mapSecondsToDatetime(start_date, pow(2,32))) == 0);
}

void Tests::testFloatCoder(){
    std::cout << "Tests::testFloatCoder" << std::endl;
    Path coded_path = Path(TestsCoder::TEST_OUTPUT_PATH, "testFloat.code");

    BitStreamWriter bit_stream_writer = BitStreamWriter(coded_path);
    float a = 0.238728932739; bit_stream_writer.pushFloat(a);
    float b = 0.2893232; bit_stream_writer.pushFloat(b);
    float c = 203020323.22; bit_stream_writer.pushFloat(c);
    float d = FLT_MAX; bit_stream_writer.pushFloat(d);
    bit_stream_writer.close();

    BitStreamReader bit_stream_reader = BitStreamReader(coded_path);
    float diff = 0.00000000000000000000000000000001;
    float a_deco = bit_stream_reader.getFloat(); assert(a_deco - a < diff);
    float b_deco = bit_stream_reader.getFloat(); assert(b_deco - b < diff);
    float c_deco = bit_stream_reader.getFloat(); assert(c_deco - c < diff);
    float d_deco = bit_stream_reader.getFloat(); assert(d_deco == d);
}
