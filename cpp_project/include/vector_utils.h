
#ifndef CPP_PROJECT_VECTOR_UTILS_H
#define CPP_PROJECT_VECTOR_UTILS_H

#include <sstream>

class VectorUtils {

public:
    static void printStringVector(std::vector<std::string> string_vector){
        for (auto const& c : string_vector)
            std::cout << c << ' ';
        std::cout << std::endl;
    }

    //
    // SOURCE: https://stackoverflow.com/a/1430774/4547232
    //
//    static std::string joinVector(std::vector<std::string> string_vector, std::string separator){
//        std::stringstream ss;
//        for(size_t i = 0; i < string_vector.size(); ++i)
//        {
//            if(i != 0) ss << separator;
//            ss << string_vector[i];
//        }
//        std::string s = ss.str();
//    }
};

#endif //CPP_PROJECT_VECTOR_UTILS_H
