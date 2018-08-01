#include "constants.h"


const std::string Constants::NO_DATA = "N";
const char Constants::NO_DATA_CHAR = 'N';
const bool Constants::MASK_MODE = false;
const int Constants::MASK_BITS = 8;
const int Constants::MASK_MAX_SIZE = 128;

bool Constants::isNoData(std::string csv_value) {
    return csv_value[0] == NO_DATA_CHAR;
}
