
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
    void goToStart();

public:
    int total_lines;
    std::string current_line;
    bool continue_reading;
    std::string full_path;

    TextReader(std::string path, std::string filename);
    std::string readLine(); // PRE: continue_reading
    void goToLine(int line_number); // PRE: line_number <= total_lines
    bool findLine(std::string string_to_find);
    void close();
};

#endif //CPP_PROJECT_TEXT_READER_H
