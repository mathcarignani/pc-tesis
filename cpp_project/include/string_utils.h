
#ifndef CPP_PROJECT_STRING_UTILS_H
#define CPP_PROJECT_STRING_UTILS_H

#include <string>
#include <vector>

class StringUtils {

public:
    static std::vector<std::string> split(std::string str, std::string token);

    static std::string join(std::vector<std::string> arr, std::string token);

    static std::string RemoveChars(const std::string& source, const std::string& chars);
};
#endif //CPP_PROJECT_STRING_UTILS_H
