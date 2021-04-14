#include "constants.h"

#include <iostream>
#include "string_utils.h"

const std::string Constants::NO_DATA = "N";
const char Constants::NO_DATA_CHAR = 'N';
const double Constants::NO_DATA_DOUBLE = 0;

const int Constants::MASK_BITS = 8;
const int Constants::MASK_MAX_SIZE = 256;

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

int Constants::getCoderValue(std::string coder_name) {
    if      (coder_name == "CoderBase")         { return 0; }
    else if (coder_name == "CoderPCA")          { return 10; }
    else if (coder_name == "CoderAPCA")         { return 11; }
    else if (coder_name == "CoderPWLH")         { return 20; }
    else if (coder_name == "CoderPWLHInt")      { return 21; }
    else if (coder_name == "CoderCA")           { return 22; }
    else if (coder_name == "CoderSF")           { return 23; }
    else if (coder_name == "CoderFR")           { return 24; }
    else if (coder_name == "CoderGAMPS")        { return 30; }
    else if (coder_name == "CoderGAMPSLimit")   { return 31; }

    std::cout << "ERROR: invalid coder_name: " << coder_name << std::endl;
    exit(1);
}

std::string Constants::getCoderName(int coder_value) {
    if      (coder_value == 0)  { return "CoderBase"; }
    else if (coder_value == 10) { return "CoderPCA"; }
    else if (coder_value == 11) { return "CoderAPCA"; }
    else if (coder_value == 20) { return "CoderPWLH"; }
    else if (coder_value == 21) { return "CoderPWLHInt"; }
    else if (coder_value == 22) { return "CoderCA"; }
    else if (coder_value == 23) { return "CoderSF"; }
    else if (coder_value == 24) { return "CoderFR"; }
    else if (coder_value == 30) { return "CoderGAMPS"; }
    else if (coder_value == 31) { return "CoderGAMPSLimit"; }

    std::cout << "ERROR: invalid coder_value: " << coder_value << std::endl;
    exit(1);
}
