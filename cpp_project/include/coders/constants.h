
#ifndef CPP_PROJECT_CONSTANTS_H
#define CPP_PROJECT_CONSTANTS_H

// MASK_MODE = 0 => the algorithm needs to process the no_data values
// MASK_MODE = 1 => the algorithm can assume there will be no no_data values
#define MASK_MODE 1
#define GOLOMB_MODE 0
#define COUT 1
#define CHECKS 1

#include <string>

class Constants {

public:
    static const std::string NO_DATA;
    static const char NO_DATA_CHAR;
    static const int MASK_BITS;
    static const int MASK_MAX_SIZE;

    static const int CODER_BASIC; // 0
    static const int CODER_PCA; // 10
    static const int CODER_APCA; // 11
    static const int CODER_PWLH; // 20
    static const int CODER_PWLH_INT; // 21
    static const int CODER_CA; // 22
    static const int CODER_FR; // 23
    static const int CODER_SF; // 24
    static const int CODER_GAMPS; // 30

    static bool isNoData(std::string csv_value);
};

#endif //CPP_PROJECT_CONSTANTS_H
