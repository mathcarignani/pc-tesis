
#include "csv_writer.h"
#include "string_utils.h"

#include <iostream>

CSVWriter::CSVWriter(std::string path, std::string filename){
    full_path = path + "/" + filename;
    file.open(full_path);
}

void CSVWriter::writeRow(std::vector<std::string> row){
    current_line_count++;
//    if (current_line_count == 1){
//        std::cout << "writeRow" << std::endl;
//        std::cout << "row[0]" << std::endl;
//        std::cout << row[0].size() << "=>" << row[0] << std::endl;
//        std::cout << "row[1]" << std::endl;
//        std::cout << row[1].size() << "=>" << row[1] << std::endl;
//        for(int i=0; i < row[1].size(); i++){
//            std::cout << row[1][i] << "-" << StringUtils::charToInt(row[1][i]) << " " << std::endl;
//        }
//        std::cout << std::endl;
//        std::cout << std::endl;
//    }
    std::string line = StringUtils::join(row, ",");
    file << line; // << std::endl;
//    unsigned char b = 0xD;
//    file << b;
    file << '\n';

}

void CSVWriter::writeRowDecoder(std::vector<std::string> row){
    current_line_count++;
    std::string line = StringUtils::join(row, ",");
    file << line; // << std::endl;
    unsigned char b = 0xD;
    file << b;
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
