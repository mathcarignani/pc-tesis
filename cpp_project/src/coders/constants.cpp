#include "constants.h"

#include <iostream>
#include "string_utils.h"

const std::string Constants::NO_DATA = "N";
const char Constants::NO_DATA_CHAR = 'N';
const double Constants::NO_DATA_DOUBLE = 0;

const int Constants::MASK_BITS = 8;
const int Constants::MASK_MAX_SIZE = 256;

const int Constants::CODER_BASE = 0;
const int Constants::CODER_PCA = 10;
const int Constants::CODER_APCA = 11;
const int Constants::CODER_PWLH = 20;
const int Constants::CODER_PWLH_INT = 21;
const int Constants::CODER_CA = 22;
const int Constants::CODER_FR = 23;
const int Constants::CODER_SF = 24;
const int Constants::CODER_GAMPS = 30;
const int Constants::CODER_GAMPS_LIMIT = 31;

const std::vector<std::string> Constants::CODERS_VECTOR = {"CoderBase", "CoderPCA", "CoderAPCA", "CoderPWLH",
                                                           "CoderPWLHInt", "CoderCA", "CoderSF", "CoderFR",
                                                           "CoderGAMPS", "CoderGAMPSLimit"};

bool Constants::isNoData(std::string csv_value) {
    return csv_value[0] == NO_DATA_CHAR;
}

bool Constants::isNoData(double value) {
    return value == NO_DATA_DOUBLE;
}

bool Constants::validMaskMode() {
#if MASK_MODE == 0 || MASK_MODE == 3
    return true;
#else
    std::cout << "ERROR: MASK_MODE macro must be either 0 or 3." << std::endl;
    exit(1);
#endif
}

//
// PRE: Constants::validMaskMode() is true
//
bool Constants::checkMaskMode(std::string mask_mode) {
#if MASK_MODE == 0
    if (mask_mode == "NM") { return true; }
    std::cout << "ERROR: mask_mode must be NM." << std::endl;
#elif MASK_MODE == 3
    if (mask_mode == "M") { return true; }
    std::cout << "ERROR: mask_mode must be M." << std::endl;
#endif
    exit(1);
}

bool Constants::checkCoderName(std::string coder_name) {
    if (StringUtils::stringInList(coder_name, CODERS_VECTOR)) { return true; }
    std::cout << "ERROR: invalid coder_name: " << coder_name << std::endl;
    exit(1);
}
