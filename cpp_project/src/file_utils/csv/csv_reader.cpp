
#include "csv_reader.h"

#include <iostream>
#include <vector>
#include "string_utils.h"
#include "vector_utils.h"
#include "text_utils.h"

CSVReader::CSVReader(std::string path, std::string filename, bool clean_char_){
    clean_char = clean_char_;
    total_lines = TextUtils::lineCount(path, filename);
    full_path = path + "/" + filename;
    file.open(full_path);
    current_line_count = 0;
    continue_reading = total_lines > 0;
}

std::vector<std::string> CSVReader::readLineCSV(){
    std::string current_line = readLine();
    if (current_line_count == 2){
        std::cout << "readLineCSV" << std::endl;
        std::cout << "current_line" << std::endl;
        std::cout << current_line.size() << "=>" << current_line << std::endl;
        for(int i=0; i < current_line.size(); i++){
            std::cout << current_line[i] << "-" << StringUtils::charToInt(current_line[i]) << " ";
        }
        std::cout << std::endl;
        std::cout << std::endl;
    }
    std::vector<std::string> current_line_vector = StringUtils::split(current_line, ","); // split by the comma
    if (current_line_count == 2){
        std::cout << std::endl;
        std::cout << "current_line_vector[0]" << std::endl;
        std::cout << current_line_vector[0].size() << "=>" << current_line_vector[0] << std::endl;
        std::cout << "current_line_vector[1]" << std::endl;
        std::cout << current_line_vector[1].size() << "=>" << current_line_vector[1] << std::endl;
        for(int i=0; i < current_line_vector[1].size(); i++){
            std::cout << current_line_vector[1][i] << "-" << StringUtils::charToInt(current_line_vector[1][i]) << " ";
        }
        std::cout << std::endl;
        std::cout << std::endl;
    }
    return current_line_vector;
}
