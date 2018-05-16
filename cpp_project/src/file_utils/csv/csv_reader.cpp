
#include "csv_reader.h"

#include <iostream>
#include <vector>
#include "string_utils.h"
#include "vector_utils.h"

std::vector<std::string> CSVReader::readLineCSV(){
    std::string current_line = readLine();
//    if (current_line_count == 1){
//        std::cout << "CURRENT_LINE 1 " << current_line.size() << " " << current_line << std::endl;
//    }
    current_line = StringUtils::removeLastChar(current_line);
//    if (current_line_count == 1){
//        std::cout << "CURRENT_LINE 2 " << current_line.size() << " " << current_line << std::endl;
//    }
    std::vector<std::string> current_line_vector = StringUtils::split(current_line, ","); // split by the comma
    return current_line_vector;
}
