
#include "csv_writer.h"
#include "string_utils.h"

#include <iostream>

void CSVWriter::constructor(std::string path, std::string filename){
    full_path = path + "/" + filename;
    file.open(full_path);
}

CSVWriter::CSVWriter(){}

CSVWriter::CSVWriter(std::string path, std::string filename){
    constructor(path, filename);
}

CSVWriter::CSVWriter(Path path){
    constructor(path.file_path, path.file_filename);
}

void CSVWriter::writeRow(std::vector<std::string> row){
    current_line_count++;
    std::string line = StringUtils::join(row, ",");
    file << line;
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
