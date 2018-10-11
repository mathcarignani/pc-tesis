
#ifndef CPP_PROJECT_CONSTANTS_H
#define CPP_PROJECT_CONSTANTS_H

// MASK_MODE = 0 => the algorithm needs to process the no_data values
// MASK_MODE = 1 => the algorithm can assume there will be no no_data values
#define MASK_MODE 1
#define COUT 1
#define CHECKS 1

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
