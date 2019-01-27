
#include "tests_header_coder.h"
#include "tests_utils.h"
#include "bit_stream_utils.h"
#include "assert.h"

TestsHeaderCoder::TestsHeaderCoder() {
    coded_file_path = Path(TestsUtils::OUTPUT_PATH, "tests_header_coder.out");
}

void TestsHeaderCoder::runAll(){
    std::cout << "  testColumnCodeVector()" << std::endl;  testColumnCodeVector();
    std::cout << "  testUpdateRangesGAMPS()" << std::endl; testUpdateRangesGAMPS();
}

void TestsHeaderCoder::testColumnCodeVector(){
    codeHeader(Path(TestsUtils::IRKIS_PATH, "vwc_1202.dat.csv"));
    assert(column_code_vector.size() == 2);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(0, 600), 10, 0, 601);

    codeHeader(Path(TestsUtils::NOAA_SST_PATH, "noaa-buoy-201701.csv"));
    assert(column_code_vector.size() == 2);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(0, 40000), 16, 0, 40001);

    codeHeader(Path(TestsUtils::NOAA_ADCP_PATH, "noaa-adcp-201501.csv"));
    assert(column_code_vector.size() == 2);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(-1100, 2700), 12, 1100, 3801);

    codeHeader(Path(TestsUtils::SOLAR_ANYWHERE_PATH, "solar-anywhere-2011.csv"));
    assert(column_code_vector.size() == 4);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(0, 1020), 10, 0, 1021);
    checkColumnCode(2, Range(0, 970), 10, 0, 971);
    checkColumnCode(3, Range(0, 800), 10, 0, 801);

    codeHeader(Path(TestsUtils::EL_NINO_PATH, "el-nino.csv"));
    assert(column_code_vector.size() == 8);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(-1000, 1000), 11, 1000, 2001);
    checkColumnCode(2, Range(-18000, 18000), 16, 18000, 36001);
    checkColumnCode(3, Range(-150, 150), 9, 150, 301);
    checkColumnCode(4, Range(-150, 150), 9, 150, 301);
    checkColumnCode(5, Range(0, 1000), 10, 0, 1001);
    checkColumnCode(6, Range(0, 4000), 12, 0, 4001);
    checkColumnCode(7, Range(0, 4000), 12, 0, 4001);

    codeHeader(Path(TestsUtils::NOAA_SPC_HAIL_PATH, "noaa_spc-hail.csv"));
    assert(column_code_vector.size() == 4);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(2500, 5000), 12, -2500, 2501);
    checkColumnCode(2, Range(-12500, -6700), 13, 12500, 5801);
    checkColumnCode(3, Range(0, 700), 10, 0, 701);

    codeHeader(Path(TestsUtils::NOAA_SPC_TORNADO_PATH, "noaa_spc-tornado.csv"));
    assert(column_code_vector.size() == 3);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(2400, 5000), 12, -2400, 2601);
    checkColumnCode(2, Range(-12500, -6800), 13, 12500, 5701);

    codeHeader(Path(TestsUtils::NOAA_SPC_WIND_PATH, "noaa_spc-wind.csv"));
    assert(column_code_vector.size() == 4);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(0, 5000), 13, 0, 5001);
    checkColumnCode(2, Range(-12500, 0), 14, 12500, 12501);
    checkColumnCode(3, Range(0, 2400), 12, 0, 2401);
}

void TestsHeaderCoder::testUpdateRangesGAMPS(){
    codeHeader(Path(TestsUtils::IRKIS_PATH, "vwc_1202.dat.csv"));
    dataset->updateRangesGAMPS(1);
    column_code_vector = dataset->column_code_vector;
    assert(column_code_vector.size() == 2);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(-600, 600), 11, 600, 1201);

    codeHeader(Path(TestsUtils::NOAA_SST_PATH, "noaa-buoy-201701.csv"));
    dataset->updateRangesGAMPS(1);
    column_code_vector = dataset->column_code_vector;
    assert(column_code_vector.size() == 2);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(-40000, 40000), 17, 40000, 80001);

    codeHeader(Path(TestsUtils::NOAA_ADCP_PATH, "noaa-adcp-201501.csv"));
    dataset->updateRangesGAMPS(1);
    column_code_vector = dataset->column_code_vector;
    assert(column_code_vector.size() == 2);
    checkColumnCode(0, Range(0, 131071), 17, 0, -1);
    checkColumnCode(1, Range(-3800, 3800), 13, 3800, 7601);
}

void TestsHeaderCoder::codeHeader(Path path){
    input_csv = new CSVReader(path);
    output_file = new BitStreamWriter(coded_file_path);
    dataset = new Dataset();
    HeaderCoder(input_csv, output_file).codeHeader(dataset);
    column_code_vector = dataset->column_code_vector;
    input_csv->close();
    output_file->close();
    BitStreamUtils::removeFile(coded_file_path);
}

void TestsHeaderCoder::checkColumnCode(int index, Range range, int bits, int offset, int nan){
    column_code = column_code_vector[index];
    assert(column_code->range == range);
    assert(column_code->bits == bits);
    assert(column_code->offset == offset);
    assert(column_code->nan == nan);
}
