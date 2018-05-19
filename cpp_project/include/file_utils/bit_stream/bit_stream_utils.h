
#ifndef CPP_PROJECT_BIT_STREAM_UTILS_H
#define CPP_PROJECT_BIT_STREAM_UTILS_H

#include "bit_stream_writer.h"

#include <string>

class BitStreamUtils {

public:
    // Compares two files, returns 0 if they match.
    // Otherwise it returns the index of the first different bit.
    static int compare(std::string path1, std::string filename1, std::string path2, std::string filename2);
    static int compareBytes(std::string path1, std::string filename1, std::string path2, std::string filename2);
};

#endif //CPP_PROJECT_BIT_STREAM_UTILS_H
