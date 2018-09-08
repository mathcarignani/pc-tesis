
#ifndef CPP_PROJECT_VECTOR_UTILS_H
#define CPP_PROJECT_VECTOR_UTILS_H

#include <sstream>

class VectorUtils {

public:
    static std::vector<std::string> intVectorToStringVector(std::vector<int> int_vector){
        int size = int_vector.size();
        std::vector<std::string> res(size);
        for(int i=0; i < size; i++){
            res[i] = std::to_string(int_vector[i]);
        }
        return res;
    }
};

#endif //CPP_PROJECT_VECTOR_UTILS_H
