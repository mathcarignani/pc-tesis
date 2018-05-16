
#include "csv_writer.h"
#include "string_utils.h"

#include <iostream>

CSVWriter::CSVWriter(std::string path, std::string filename){
    full_path = path + "/" + filename;
    file.open(full_path);
}

void CSVWriter::writeRow(std::vector<std::string> row){
    std::string line = StringUtils::join(row, ",");
    file << line << std::endl;
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
