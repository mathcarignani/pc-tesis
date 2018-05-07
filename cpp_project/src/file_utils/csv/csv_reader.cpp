
#include "csv_reader.h"

#include <iostream>
#include <vector>
#include "string_utils.h"
#include "csv_utils.h"

CSVReader::CSVReader(std::string path, std::string filename){
    total_lines = CSVUtils::lineCount(path, filename);
    full_path = path + "/" + filename;
    file.open(full_path);
    continue_reading = total_lines > 0;
}


//
// PRE: row_number <= total_lines
//
//void GoToRow(int row_number);
//

//
// PRE: continue_reading
//
std::vector<std::string> CSVReader::readLine(){
    std::getline(file, current_line);
    continue_reading = ++current_line_count < total_lines;
    current_line = StringUtils::RemoveChars(current_line, "\n"); // remove endline
    std::vector<std::string> current_line_vector = StringUtils::split(current_line, ","); // split by the comma
    return current_line_vector;
}

void CSVReader::close(){
    file.close();
}
