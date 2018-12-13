
#include "tests_coders.h"

#include "csv_writer.h"
#include "constants.h"
#include "scripts.h"
#include "string_utils.h"
#include "tests_coders_utils.h"
#include "tests_utils.h"

// Set to 1 to set up the tests, then set to 0
#define RECORD 0


void TestsCoders::testSideFilder() {
//     Path file_path = Path(TestsUtils::OUTPUT_PATH + "/sf", "vwc_1202.dat.csv");
    Path file_path = Path(TestsUtils::OUTPUT_PATH + "/sf", "vwc_1202.dat2.csv");

    std::vector<int> lossless{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    std::vector<int>    lossy{0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5};

    std::string coder_name = "CoderSF";
    Path output_code_path = TestsCodersUtils::codedFilePath(TestsUtils::OUTPUT_PATH, file_path, coder_name);
    Path output_decode_path = TestsCodersUtils::decodedFilePath(TestsUtils::OUTPUT_PATH, file_path, coder_name);

    std::cout << output_code_path.full_path << std::endl;
    std::cout << output_decode_path.full_path << std::endl;

//    Scripts::codeSF(file_path, output_code_path, 5, lossless);
//    Scripts::decodeSF(output_code_path, output_decode_path, 5);
//    TestsCodersUtils::compareFiles(file_path, output_decode_path);
//    std::cout << "SAME FILE!!" << std::endl;
}

void TestsCoders::testGAMPS() {
//     Path file_path = Path(TestsUtils::IRKIS_PATH, "vwc_1202.dat.csv");
//     std::vector<int> lossless{0, 0};
//     std::vector<int>    lossy{0, 5};

    Path file_path = Path(TestsUtils::NOAA_SPC_HAIL_PATH, "noaa_spc-hail.csv");
    std::vector<int> lossless{0, 0, 0, 0};
    std::vector<int>    lossy{0, 5};

    std::string coder_name = "GAMPS";
    Path output_code_path = TestsCodersUtils::codedFilePath(TestsUtils::OUTPUT_PATH, file_path, coder_name);
    Path output_decode_path = TestsCodersUtils::decodedFilePath(TestsUtils::OUTPUT_PATH, file_path, coder_name);

    std::cout << output_code_path.full_path << std::endl;
    std::cout << output_decode_path.full_path << std::endl;

    Scripts::code("CoderGAMPS", file_path, output_code_path, 5, lossless);
    Scripts::decode(output_code_path, output_decode_path);
    TestsCodersUtils::compareFiles(file_path, output_decode_path);
    std::cout << "SAME FILE!!" << std::endl;
}

void TestsCoders::testCA(){
    Path file_path = Path(TestsUtils::IRKIS_PATH, "vwc_1202.dat.csv");
    std::vector<int> lossless{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    std::vector<int>    lossy{0, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1};

    std::string coder_name = "CA";
    Path output_code_path = TestsCodersUtils::codedFilePath(TestsUtils::OUTPUT_PATH, file_path, coder_name);
    Path output_decode_path = TestsCodersUtils::decodedFilePath(TestsUtils::OUTPUT_PATH, file_path, coder_name);

    std::cout << output_code_path.full_path << std::endl;
    std::cout << output_decode_path.full_path << std::endl;

    Scripts::code("CoderCA", file_path, output_code_path, 5, lossy);
    Scripts::decode(output_code_path, output_decode_path);
//    TestsCodersUtils::compareFiles(file_path, output_decode_path);
//    std::cout << "SAME FILE!!" << std::endl;
}


TestsCoders::TestsCoders(){
    setDatasets();
}

void TestsCoders::setDatasets(){
    Path file1_path = Path(TestsUtils::IRKIS_PATH, "vwc_1202.dat.csv");
    std::vector<int> file1_lossless{0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0};
    std::vector<int>    file1_lossy{0, 12, 3, 5, 2, 4, 10, 6, 4, 3, 2};

    Path file2_path = Path(TestsUtils::SOLAR_ANYWHERE_PATH, "solar-anywhere-2012.csv");
    std::vector<int> file2_lossless{0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0};
    std::vector<int>    file2_lossy{0, 13, 14, 5, 13, 13, 5, 14, 14, 5, 13, 13, 5, 13, 13, 5, 14, 14, 5, 13, 13, 5, 13, 13, 5, 14, 14, 5, 14, 13, 5, 14, 14, 5, 14, 15, 5};

    Path file3_path = Path(TestsUtils::NOAA_SPC_HAIL_PATH, "noaa_spc-hail.csv");
    std::vector<int> file3_lossless{0,   0,   0,  0};
    std::vector<int>    file3_lossy{0, 143, 252, 16};

    paths = {file1_path, file2_path, file3_path};
    lossless = {file1_lossless, file2_lossless, file3_lossless};
    lossy = {file1_lossy, file2_lossy, file3_lossy};

    win_size = 5;
}

void TestsCoders::setCoderPaths(std::string coder_name_){
    coder_name = TestsCodersUtils::setAndWriteCoderName(coder_name_, bits_csv);
    output_code_path = TestsCodersUtils::codedFilePath(output_path_str, file_path, coder_name);
    expected_code_path = TestsCodersUtils::codedFilePath(expected_path_str, file_path, coder_name);
    output_decode_path = TestsCodersUtils::decodedFilePath(output_path_str, file_path, coder_name);
}

void TestsCoders::setModePaths(int i){
    if (mode == "LOSSLESS") {
        errors_vector = lossless[i];
        expected_path_str = expected_root_folder + "/lossless";
        output_path_str = output_root_folder + "/lossless";
    }
    else {
        errors_vector = lossy[i];
        expected_path_str = expected_root_folder + "/lossy";
        output_path_str = output_root_folder + "/lossy";
    }
}

void TestsCoders::runAll(){
    std::cout << "TestsCoder::runAll()" << std::endl;
    std::string mask_mode_folder = (MASK_MODE) ? "mask_mode_true" : "mask_mode_false";

    expected_root_folder = TestsUtils::OUTPUT_PATH + "/expected/" + mask_mode_folder;

#if RECORD
    output_root_folder = expected_root_folder;
#else
    output_root_folder = TestsUtils::OUTPUT_PATH + "/output/" + mask_mode_folder;
#endif

    Path bits_csv_path = Path(output_root_folder, "bits-out.csv");
    bits_csv = new CSVWriter(bits_csv_path);

    std::vector<std::string> modes{"LOSSLESS", "LOSSY"};

    for(int i = 0; i < paths.size(); i++){
        file_path = paths[i];
        TestsCodersUtils::writeStringCSV(bits_csv, file_path.file_filename, true);

        for(int j = 0; j < modes.size(); j++){
            mode = modes[j];
            TestsCodersUtils::writeStringCSV(bits_csv, mode, false);
            setModePaths(i);

            if (mode == "LOSSLESS"){ testCoderBasic(); }
            testCoder("CoderPCA");
            testCoder("CoderAPCA");
            testCoder("CoderPWLHInt");
            testCoder("CoderPWLH");
             testCoder("CoderCA");

        #if MASK_MODE
            testCoder("CoderFR");
            // TODO: fix coder SF
            // testCoder("CoderSF");
        #endif
        }
    }
    // compare bits files
    bits_csv->close();
    Path expected_bits_csv_path = Path(expected_root_folder, "bits-out.csv");
    TestsCodersUtils::compareFiles(expected_bits_csv_path, bits_csv_path);
}

void TestsCoders::testCoderBasic(){
    setCoderPaths("CoderBasic");
    ds = Scripts::codeBasic(file_path, output_code_path);
    TestsCodersUtils::writeBitsCSV(bits_csv, ds);
    TestsCodersUtils::compareFiles(output_code_path, expected_code_path);
    Scripts::decode(output_code_path, output_decode_path);
    TestsCodersUtils::compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);
}

void TestsCoders::testCoder(std::string coder_name){
    setCoderPaths(coder_name);
    ds = Scripts::code(coder_name, file_path, output_code_path, win_size, errors_vector);
    TestsCodersUtils::writeBitsCSV(bits_csv, ds);
    TestsCodersUtils::compareFiles(output_code_path, expected_code_path);
    Scripts::decode(output_code_path, output_decode_path);
    TestsCodersUtils::compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);
}
