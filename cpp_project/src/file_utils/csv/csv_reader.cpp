
#include "csv_reader.h"

#include <iostream>
#include <vector>
#include "string_utils.h"
#include "vector_utils.h"
#include "text_utils.h"

void CSVReader::constructor(std::string path, std::string filename){
    total_lines = TextUtils::lineCount(path, filename);
    full_path = path + "/" + filename;
    file.open(full_path);
    current_line_count = 0;
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

std::string CSVReader::readLineCSVWithIndex(int index){
    std::string current_line = readLine();
    std::string col_value = StringUtils::splitByCharWithIndex(current_line, ',', index);
    return col_value;
};

void CSVReader::goToFirstDataRow(){
    goToLine(4);
}
