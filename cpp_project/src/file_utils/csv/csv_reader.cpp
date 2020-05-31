
#include "csv_reader.h"

#include <iostream>
#include <vector>
#include "string_utils.h"
#include "vector_utils.h"
#include "text_utils.h"

void CSVReader::constructor(std::string path, std::string filename){
    full_path = path + "/" + filename;
    file.open(full_path);
    if (!file.is_open()){
        std::cout << "CSVReader: Error opening file: " << full_path << std::endl;
        exit(-1);
    }
    current_line_count = 0;
    total_lines = TextUtils::lineCount(path, filename);
    continue_reading = total_lines > 0;
}

CSVReader::CSVReader(Path path){
    constructor(path.file_path, path.file_filename);
}

std::vector<std::string> CSVReader::readLineCSV(){
    std::string current_line = readLine();
    std::vector<std::string> current_line_vector = StringUtils::splitByChar(current_line, ','); // split by the comma
    return current_line_vector;
}

std::string CSVReader::readNextValue(){
    std::string current_line = readLine();
    std::string col_value = StringUtils::splitByCharWithIndex(current_line, ',', column_index);
    return col_value;
};

void CSVReader::goToFirstDataRow(int column_index_){
    column_index = column_index_;
    goToLine(4);
}
