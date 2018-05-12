
#include "text_reader.h"

#include "assert.h"
#include "text_utils.h"

TextReader::TextReader(std::string path, std::string filename){
    total_lines = TextUtils::lineCount(path, filename);
    full_path = path + "/" + filename;
    file.open(full_path);
    current_line_count = 0;
    continue_reading = total_lines > 0;
}

std::string TextReader::readLine(){
    assert(continue_reading);

    readLineAux();
    return current_line;
}

void TextReader::goToRow(int row_number){
    assert(row_number <= total_lines);

    file.clear();
    file.seekg(0, std::ios::beg);
    current_line_count = 0;
    continue_reading = total_lines > 0;
    for(int i=0; i < row_number; i++) { readLineAux(); }
}

void TextReader::readLineAux() {
    std::getline(file, current_line);
    current_line_count++;
    continue_reading = current_line_count < total_lines;
}

void TextReader::close(){
    file.close();
}
