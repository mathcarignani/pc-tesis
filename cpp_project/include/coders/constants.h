
#ifndef CPP_PROJECT_CONSTANTS_H
#define CPP_PROJECT_CONSTANTS_H

#define MASK_MODE 0

#include <string>

class Constants {

public:
    static const std::string NO_DATA;
    static const char NO_DATA_CHAR;
    static const int MASK_BITS;
    static const int MASK_MAX_SIZE;

    static bool isNoData(std::string csv_value);
};

#endif //CPP_PROJECT_CONSTANTS_H
