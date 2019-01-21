
#ifndef CPP_PROJECT_VECTOR_UTILS_H
#define CPP_PROJECT_VECTOR_UTILS_H

#include <sstream>
#include "string_utils.h"
#include <cstring>
#include <vector>
#include <algorithm>
#include <iostream>

class VectorUtils {

private:
    template <typename T>
    static void printVector(T vector){
        std::cout << "[";
        int size = vector.size();
        for(int i=0; i < size; i++){
            std::cout << vector[i];
            if (i != size - 1) { std::cout << ", "; }
        }
        std::cout << "]" << std::endl;
    }

public:
    static std::string intVectorToString(std::vector<int> int_vector){
        int size = int_vector.size();
        std::string res = "";
        for(int i=0; i < size; i++){
            std::string str = StringUtils::intToString(int_vector[i]);
            if (i != size - 1){
                str += ",";
            }
            res += str;
        }
        return res;
    }

    static std::vector<std::string> intVectorToStringVector(std::vector<int> int_vector){
        int size = int_vector.size();
        std::vector<std::string> res(size);
        for(int i=0; i < size; i++){
            res[i] = StringUtils::intToString(int_vector[i]);
        }
        return res;
    }

    static void printIntVector(std::vector<int> vector){
        printVector(vector);
    }

    static void printStringVector(std::vector<std::string> vector){
        printVector(vector);
    }

    static bool vectorIncludesInt(std::vector<int> int_vector, int element){
        return (std::find(int_vector.begin(), int_vector.end(), element) != int_vector.end());
    }

    static std::vector<int> removeOccurrences(std::vector<int> int_vector, int integer){
        std::vector<int> new_vector;
        for(int i=0; i < int_vector.size(); i++){
            int element = int_vector.at(i);
            if (element == integer) { continue; }
            new_vector.push_back(element);
        }
        return new_vector;
    }
};

#endif //CPP_PROJECT_VECTOR_UTILS_H
