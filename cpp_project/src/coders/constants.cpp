#include "constants.h"

#include <iostream>

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

bool Constants::isNoData(std::string csv_value) {
    return csv_value[0] == NO_DATA_CHAR;
}

bool Constants::isNoData(double value) {
    return value == NO_DATA_DOUBLE;
}

bool Constants::validMaskMode() {
#if MASK_MODE >= 0 && MASK_MODE <= 3
    return true;
#else
    std::cout << "ERROR: MASK_MODE must be 0, 1, 2, or 3." << std::endl;
    exit(1);
#endif
}

//
// PRE: Constants::validMaskMode() is true
//
bool Constants::checkMaskMode(std::string mask_mode) {
#if MASK_MODE == 0
    if (mask_mode == "0") { return true; }
    std::cout << "ERROR: mask_mode must be 0." << std::endl;
#elif MASK_MODE == 1
    if (mask_mode == "1") { return true; }
    std::cout << "ERROR: mask_mode must be 1." << std::endl;
#elif MASK_MODE == 2
    if (mask_mode == "2") { return true; }
    std::cout << "ERROR: mask_mode must be 2." << std::endl;
#elif MASK_MODE == 3
    if (mask_mode == "3") { return true; }
    std::cout << "ERROR: mask_mode must be 3." << std::endl;
#endif
    exit(1);
}
