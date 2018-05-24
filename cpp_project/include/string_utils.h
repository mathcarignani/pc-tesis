
#ifndef CPP_PROJECT_STRING_UTILS_H
#define CPP_PROJECT_STRING_UTILS_H

#include <string>
#include <vector>

class StringUtils {

public:
    static bool find(std::string string, std::string string_to_find);
    static std::vector<std::string> splitByString(std::string str, std::string delimiter);
    static std::vector<std::string> splitByChar(std::string str, const char delimiter);
    static std::string splitByCharWithIndex(std::string str, const char delimiter, int index);
    static std::string join(std::vector<std::string> arr, std::string token);
    static std::string removeChars(const std::string& source, const std::string& chars);
    static std::string removeLastChar(const std::string& source);
    static int charToInt(const char character);
    static const char intToChar(const int integer);
    static int bitLength(uint32_t value);
    static int doubleToInt(double d);
    static std::string doubleToString(double d);
};

#endif //CPP_PROJECT_STRING_UTILS_H
