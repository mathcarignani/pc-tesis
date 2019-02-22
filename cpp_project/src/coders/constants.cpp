#include "constants.h"


const std::string Constants::NO_DATA = "N";
const char Constants::NO_DATA_CHAR = 'N';
const double Constants::NO_DATA_DOUBLE = 0;

const int Constants::MASK_BITS = 8;
const int Constants::MASK_MAX_SIZE = 256;

const int Constants::CODER_BASIC = 0;
const int Constants::CODER_PCA = 10;
const int Constants::CODER_APCA = 11;
const int Constants::CODER_PWLH = 20;
const int Constants::CODER_PWLH_INT = 21;
const int Constants::CODER_CA = 22;
const int Constants::CODER_FR = 23;
const int Constants::CODER_SF = 24;
const int Constants::CODER_GAMPS = 30;

bool Constants::isNoData(std::string csv_value) {
    return csv_value[0] == NO_DATA_CHAR;
}
