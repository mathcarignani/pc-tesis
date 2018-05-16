
#ifndef CPP_PROJECT_VECTOR_UTILS_H
#define CPP_PROJECT_VECTOR_UTILS_H

class VectorUtils {

public:
    static void printStringVector(std::vector<std::string> string_vector){
        for (auto const& c : string_vector)
            std::cout << c << ' ';
        std::cout << std::endl;
    }
};

#endif //CPP_PROJECT_VECTOR_UTILS_H
