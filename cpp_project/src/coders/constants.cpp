#include "constants.h"


const std::string Constants::NO_DATA = "N";
const char Constants::NO_DATA_CHAR = 'N';
const int Constants::MASK_BITS = 8;
const int Constants::MASK_MAX_SIZE = 256;

bool Constants::isNoData(std::string csv_value) {
    return csv_value[0] == NO_DATA_CHAR;
}
