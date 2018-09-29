
#include "csv_utils.h"

#include <fstream>
#include <iostream>
#include <vector>
#include "csv_reader.h"
#include "csv_writer.h"
#include "assert.h"
#include "vector_utils.h"
#include "string_utils.h"

void CSVUtils::CopyCSV(Path input_path, Path output_path){
    CSVReader* csv_reader = new CSVReader(input_path);
    CSVWriter* csv_writer = new CSVWriter(output_path);
    while (csv_reader->continue_reading) {
        std::vector<std::string> row = csv_reader->readLineCSV();
        std::string row_str = StringUtils::join(row, ",");
        std::vector<std::string> row_str_split = StringUtils::splitByString(row_str, ",");
//        if (csv_reader.current_line_count == 2){
//            std::cout << "row_str" << std::endl;
//            std::cout << row_str.size() << std::endl;
//            std::cout << row_str << std::endl;
//            std::cout << "##################################" << std::endl;
//            std::vector<std::string> row_str_split = {"TIME UNIT:", "minutes"};
//        }
        csv_writer->writeRow(row_str_split);
    }
    delete csv_reader;
    delete csv_writer;
}

void CSVUtils::CompareCSVLossless(Path path1, Path path2){
    CSVReader* csv_reader1 = new CSVReader(path1);
    CSVReader* csv_reader2 = new CSVReader(path2);
//    assert(csv_reader1.total_lines == csv_reader2.total_lines);
    while (csv_reader1->continue_reading) {
        std::vector<std::string> row1 = csv_reader1->readLineCSV();
        std::vector<std::string> row2 = csv_reader2->readLineCSV();
        if (row1 != row2){
            std::cout << "current_line " << csv_reader1->current_line_count << std::endl;
            std::cout << "line1 = " << StringUtils::join(row1, ".") << std::endl;
            std::cout << "line2 = " << StringUtils::join(row2, ".") << std::endl;
            break;
        }
    }
    delete csv_reader1;
    delete csv_reader2;
}
