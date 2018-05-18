
#include "csv_reader.h"

#include <iostream>
#include <vector>
#include "string_utils.h"
#include "vector_utils.h"

std::vector<std::string> CSVReader::readLineCSV(){
    std::string current_line = readLine();
//    current_line.pop_back();
    std::vector<std::string> current_line_vector = StringUtils::split(current_line, ","); // split by the comma

//    if (current_line_count < 5){
//        std::cout << "read line" << std::endl;
//        std::cout << current_line.size() << std::endl;
//        std::cout << current_line << std::endl;
//        std::cout << current_line_vector.size() << std::endl;
//
//        for(int i=0; i < current_line_vector.size(); i++){
//            std::cout << "i=" << i << std::endl;
//            std::cout << current_line_vector[i].size() << std::endl;
//            std::cout << current_line_vector[i] << std::endl;
//        }
//    }
    return current_line_vector;
}
