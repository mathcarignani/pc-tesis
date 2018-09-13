
#ifndef CPP_PROJECT_VECTOR_UTILS_H
#define CPP_PROJECT_VECTOR_UTILS_H

#include <sstream>
#include "string_utils.h"

class VectorUtils {

public:
    static std::vector<std::string> intVectorToStringVector(std::vector<int> int_vector){
        int size = int_vector.size();
        std::vector<std::string> res(size);
        for(int i=0; i < size; i++){
            res[i] = StringUtils::intToString(int_vector[i]);
        }
        return res;
    }

    static void printIntVector(std::vector<int> int_vector){
        std::cout << "[";
        int size = int_vector.size();
        for(int i=0; i < size; i++){
            std::cout << int_vector[i];
            if (i != size - 1) { std::cout << ", "; }
        }
        std::cout << "]" << std::endl;
    }

    static bool vectorIncludesInt(std::vector<int> int_vector, int element){
        return (std::find(int_vector.begin(), int_vector.end(), element) != int_vector.end());
    }
};

#endif //CPP_PROJECT_VECTOR_UTILS_H
