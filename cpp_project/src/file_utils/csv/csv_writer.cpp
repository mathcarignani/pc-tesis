
#include "csv_writer.h"
#include "string_utils.h"

#include <iostream>

CSVWriter::CSVWriter(std::string path, std::string filename){
    full_path = path + "/" + filename;
    file.open(full_path);
}

void CSVWriter::writeRow(std::vector<std::string> row){
//    if (row.size() == 2){
//        std::cout << "row[0]" << std::endl;
//        std::cout << row[0].size() << std::endl;
//        std::cout << row[0] << std::endl;
//        std::cout << "row[1]" << std::endl;
//        std::cout << row[1].size() << std::endl;
//        std::cout << row[1] << std::endl;
//    }
    std::string line = StringUtils::join(row, ",");
//    if (row.size() == 2){
//        std::cout << line << std::endl;
//        for(int i=0; i < line.size(); i++){
//            std::cout << "-[" << i << "]" << StringUtils::charToInt(line[i]);
//        }
//        std::cout << std::endl;
////
////        std::cout << line.size() << std::endl;
////        std::cout << line << std::endl;
//    }
    file << line; // << std::endl;
    file << '\n';
}

void CSVWriter::close(){
    file.close();
}


//class CSVWriter {
//
//public:
//
//    CSVWriter(std::string path, std::string filename);
//
//    void writeRow(std::vector<std::string> row);
//
//    void close();
//};
