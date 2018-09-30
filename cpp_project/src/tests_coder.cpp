
#include "tests_coder.h"

#include "csv_writer.h"
#include "constants.h"
#include "scripts.h"
#include "vector_utils.h"
#include "bit_stream_utils.h"
#include "assert.h"
#include "string_utils.h"
#include "csv_utils.h"
#include "os_utils.h"

// Set to 1 to set up the tests, then set to 0
#define RECORD 0

const std::string TestsCoder::DATASETS_PATH = OSUtils::DATASETS_CSV_PATH;
const std::string TestsCoder::TEST_OUTPUT_PATH = OSUtils::CPP_PROJECT_PATH + "/test_files";

void TestsCoder::testSideFilderCoder() {
    Path file_path = Path(DATASETS_PATH + "/[1]irkis", "vwc_1202.dat.csv");
    std::vector<int> lossless{0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0};
    std::vector<int>    lossy{0, 12, 3, 5, 2, 4, 10, 6, 4, 3, 2};

    std::string coder_name = "CoderSF";
    Path output_code_path = codedFilePath(TEST_OUTPUT_PATH, file_path, coder_name);
    Path output_decode_path = decodedFilePath(TEST_OUTPUT_PATH, file_path, coder_name);

    Scripts::codeSF(file_path, output_code_path, 5, lossy);
    Scripts::decodeSF(output_code_path, output_decode_path, 5);
}


void TestsCoder::testCoderDecoder(){
    std::cout << "Tests::testCoderDecoder" << std::endl;
    std::string mask_mode_folder = (MASK_MODE) ? "mask_mode_true" : "mask_mode_false";

    std::string expected_root_folder = TEST_OUTPUT_PATH + "/expected/" + mask_mode_folder;

#if RECORD
    std::string output_root_folder = expected_root_folder;
#else
    std::string output_root_folder = TEST_OUTPUT_PATH + "/output/" + mask_mode_folder;
#endif

    Path bits_csv_path = Path(output_root_folder, "bits-out.csv");
    CSVWriter bits_csv = CSVWriter(bits_csv_path);

    Path file1_path = Path(DATASETS_PATH + "/[1]irkis", "vwc_1202.dat.csv");
    std::vector<int> file1_lossless{0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0};
    std::vector<int>    file1_lossy{0, 12, 3, 5, 2, 4, 10, 6, 4, 3, 2};

    Path file2_path = Path(DATASETS_PATH + "/[4]solar-anywhere/all", "solar-anywhere-2012.csv");
    std::vector<int> file2_lossless{0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0,  0,  0, 0};
    std::vector<int>    file2_lossy{0, 13, 14, 5, 13, 13, 5, 14, 14, 5, 13, 13, 5, 13, 13, 5, 14, 14, 5, 13, 13, 5, 13, 13, 5, 14, 14, 5, 14, 13, 5, 14, 14, 5, 14, 15, 5};

    Path file3_path = Path(DATASETS_PATH + "/[6]noaa-spc-reports/hail", "noaa_spc-hail.csv");
    std::vector<int> file3_lossless{0,   0,   0,  0};
    std::vector<int>    file3_lossy{0, 143, 252, 16};

    std::vector<Path> paths{file1_path, file2_path, file3_path};
    std::vector<std::vector<int>> lossless{file1_lossless, file2_lossless, file3_lossless};
    std::vector<std::vector<int>> lossy{file1_lossy, file2_lossy, file3_lossy};

    std::vector<std::string> modes{"LOSSLESS", "LOSSY"};

    for(int i = 0; i < paths.size(); i++){
        Path file_path = paths[i];
        writeStringCSV(bits_csv, file_path.file_filename, true);

        for(int j = 0; j < modes.size(); j++){
            std::string mode = modes[j];
            writeStringCSV(bits_csv, mode, false);

            std::vector<int> errors_vector;
            std::string expected_path_str, output_path_str;

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

            Path expected_code_path, output_code_path, output_decode_path;
            std::string coder_name;
            Dataset ds;

            if (mode == "LOSSLESS"){
                // Coder Basic
                coder_name = setAndWriteCoderName("CoderBasic", bits_csv);
                output_code_path = codedFilePath(output_path_str, file_path, coder_name);
                expected_code_path = codedFilePath(expected_path_str, file_path, coder_name);
                output_decode_path = decodedFilePath(output_path_str, file_path, coder_name);

                ds = Scripts::codeBasic(file_path, output_code_path); writeBitsCSV(bits_csv, ds); // CODE
                compareFiles(output_code_path, expected_code_path);
                Scripts::decodeBasic(output_code_path, output_decode_path); // DECODE
                compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);
            }

            // Coder PCA
            coder_name = setAndWriteCoderName("CoderPCA", bits_csv);
            output_code_path = codedFilePath(output_path_str, file_path, coder_name);
            expected_code_path = codedFilePath(expected_path_str, file_path, coder_name);
            output_decode_path = decodedFilePath(output_path_str, file_path, coder_name);

            ds = Scripts::codePCA(file_path, output_code_path, 5, errors_vector); writeBitsCSV(bits_csv, ds); // CODE
            compareFiles(output_code_path, expected_code_path);
            Scripts::decodePCA(output_code_path, output_decode_path, 5); // DECODE
            compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);

            // Coder APCA
            coder_name = setAndWriteCoderName("CoderAPCA", bits_csv);
            output_code_path = codedFilePath(output_path_str, file_path, coder_name);
            expected_code_path = codedFilePath(expected_path_str, file_path, coder_name);
            output_decode_path = decodedFilePath(output_path_str, file_path, coder_name);

            ds = Scripts::codeAPCA(file_path, output_code_path, 5, errors_vector); writeBitsCSV(bits_csv, ds); // CODE
            compareFiles(output_code_path, expected_code_path);
            Scripts::decodeAPCA(output_code_path, output_decode_path, 5); // DECODE
            compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);

            // Coder PWLHInt
            coder_name = setAndWriteCoderName("CoderPWLHInt", bits_csv);
            output_code_path = codedFilePath(output_path_str, file_path, coder_name);
            expected_code_path = codedFilePath(expected_path_str, file_path, coder_name);
            output_decode_path = decodedFilePath(output_path_str, file_path, coder_name);

            ds = Scripts::codePWLH(file_path, output_code_path, 5, errors_vector, true); writeBitsCSV(bits_csv, ds); // CODE
            compareFiles(output_code_path, expected_code_path);
            Scripts::decodePWLH(output_code_path, output_decode_path, 5, true); // DECODE
            compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);

            // Coder PWLH
            coder_name = setAndWriteCoderName("CoderPWLH", bits_csv);
            output_code_path = codedFilePath(output_path_str, file_path, coder_name);
            expected_code_path = codedFilePath(expected_path_str, file_path, coder_name);
            output_decode_path = decodedFilePath(output_path_str, file_path, coder_name);

            ds = Scripts::codePWLH(file_path, output_code_path, 5, errors_vector, false); writeBitsCSV(bits_csv, ds); // CODE
            compareFiles(output_code_path, expected_code_path);
            Scripts::decodePWLH(output_code_path, output_decode_path, 5, false); // DECODE
            compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);

//            // Coder CA
//            coder_name = setAndWriteCoderName("CoderCA", bits_csv);
//            output_code_path = codedFilePath(output_path_str, file_path, coder_name);
//            expected_code_path = codedFilePath(expected_path_str, file_path, coder_name);
//            output_decode_path = decodedFilePath(output_path_str, file_path, coder_name);
//
//            ds = Scripts::codeCA(file_path, output_code_path, 5, errors_vector); writeBitsCSV(bits_csv, ds); // CODE
//            compareFiles(output_code_path, expected_code_path);
//            Scripts::decodeCA(output_code_path, output_decode_path, 5); // DECODE
//            compareDecodedFiles(mode, file_path, output_decode_path, expected_path_str, coder_name);
        }
    }
    // compare bits files
    bits_csv.close();
    Path expected_bits_csv_path = Path(expected_root_folder, "bits-out.csv");
    compareFiles(expected_bits_csv_path, bits_csv_path);
}

std::string TestsCoder::setAndWriteCoderName(std::string coder_name, CSVWriter & csv_writer){
    std::cout << ">> " << coder_name << std::endl;
    csv_writer.writeRow({coder_name});
    return coder_name;
}

void TestsCoder::writeBitsCSV(CSVWriter & csv_writer, Dataset dataset){
    csv_writer.writeRow(VectorUtils::intVectorToStringVector(dataset.totalMaskBitsArray()));
    csv_writer.writeRow(VectorUtils::intVectorToStringVector(dataset.totalBitsArray()));
}

void TestsCoder::writeStringCSV(CSVWriter & csv_writer, std::string mode, bool title){
    std::cout << ">> " << mode << std::endl;
    if (title){
        csv_writer.writeRow({""});
    }
    csv_writer.writeRow({""});
    csv_writer.writeRow({mode});
    csv_writer.writeRow({""});
}

Path TestsCoder::codedFilePath(std::string folder, Path file_path, std::string coder_name){
    return Path(folder, file_path.file_filename + "-" + coder_name + "-Code");
}

Path TestsCoder::decodedFilePath(std::string folder, Path file_path, std::string coder_name){
    return Path(folder, file_path.file_filename + "-" + coder_name + "-Decode.csv");
}

void TestsCoder::compareDecodedFiles(std::string mode, Path file_path, Path output_decode_path, std::string expected_path_str, std::string coder_name){
    if (mode == "LOSSLESS"){
        // original_file should be the same as decoded(coded(original_file))
        compareFiles(file_path, output_decode_path);
        BitStreamUtils::removeFile(output_decode_path);
    }
    else {
        Path expected_decode_path = decodedFilePath(expected_path_str, file_path, coder_name);
        compareFiles(expected_decode_path, output_decode_path);
    }
}

void TestsCoder::compareFiles(Path path1, Path path2){
    int res = BitStreamUtils::compareBytes(path1, path2);
    if (res !=0 ){
        std::cout << "FAILURE!" << std::endl;
        std::cout << "File 1 = " << path1.full_path << std::endl;
        std::cout << "File 2 = " << path2.full_path << std::endl;
        std::cout << "First diff byte = " << res << std::endl;

        std::vector<std::string> filename1_split = StringUtils::splitByChar(path1.file_filename, '.');
        std::vector<std::string> filename2_split = StringUtils::splitByChar(path2.file_filename, '.');
        std::string file1_ext = filename1_split[filename1_split.size()-1];
        std::string file2_ext = filename2_split[filename2_split.size()-1];

        if (file1_ext == "csv" && file2_ext == "csv"){
            std::cout << "Compare CSV..." << std::endl;
            CSVUtils::CompareCSVLossless(path1, path2);
        }

    }
    assert(res == 0);
}
