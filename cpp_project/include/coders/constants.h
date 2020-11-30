
#ifndef CPP_PROJECT_CONSTANTS_H
#define CPP_PROJECT_CONSTANTS_H

//
// MASK_MODE == 0 => the algorithm needs to process the no_data values (NM)
//
// MASK_MODE  > 0 => the algorithm can assume there will be no no_data values
// MASK_MODE == 1 => simple coder
// MASK_MODE == 2 => golomb coder
// MASK_MODE == 3 => arithmetic coder (M)
//
#define COUT 1
#define CHECKS 0
#define RECORD_TESTS 0 // Set to 1 to set up the tests, then set to 0

#include <string>
#include <vector>

class Constants {

public:
    static const std::string NO_DATA;
    static const char NO_DATA_CHAR;
    static const double NO_DATA_DOUBLE;

    static const int MASK_BITS;
    static const int MASK_MAX_SIZE;

    static const int CODER_BASE; // 0
    static const int CODER_PCA; // 10
    static const int CODER_APCA; // 11
    static const int CODER_PWLH; // 20
    static const int CODER_PWLH_INT; // 21
    static const int CODER_CA; // 22
    static const int CODER_FR; // 23
    static const int CODER_SF; // 24
    static const int CODER_GAMPS; // 30
    static const int CODER_GAMPS_LIMIT; // 31

    static const std::vector<std::string> CODERS_VECTOR;

    static bool isNoData(std::string csv_value);
    static bool isNoData(double value);

    static bool validMaskMode();
    static bool checkMaskMode(std::string mask_mode);

    static bool checkCoderName(std::string coder_name);
};

#endif //CPP_PROJECT_CONSTANTS_H
