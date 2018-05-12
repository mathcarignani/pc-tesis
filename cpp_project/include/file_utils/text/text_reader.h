
#ifndef CPP_PROJECT_TEXT_READER_H
#define CPP_PROJECT_TEXT_READER_H

#include <fstream>
#include <string>


class TextReader {

private:
    std::ifstream file;
    int current_line_count;

protected:
    void readLineAux();

public:
    int total_lines;
    std::string current_line;
    bool continue_reading;
    std::string full_path;

    TextReader(std::string path, std::string filename);
    // PRE: continue_reading
    std::string readLine();
    // PRE: row_number <= total_lines
    void goToRow(int row_number);
    void close();
};

#endif //CPP_PROJECT_TEXT_READER_H
