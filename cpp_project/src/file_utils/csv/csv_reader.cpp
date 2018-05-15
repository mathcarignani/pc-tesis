
#include "csv_reader.h"

#include <iostream>
#include <vector>
#include "string_utils.h"

std::vector<std::string> CSVReader::readLineCSV(){
    std::string current_line = readLine();
    current_line = StringUtils::removeLastChar(current_line);
    std::vector<std::string> current_line_vector = StringUtils::split(current_line, ","); // split by the comma
    return current_line_vector;
}
