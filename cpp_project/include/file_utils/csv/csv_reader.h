
#ifndef CPP_PROJECT_CSV_READER_H
#define CPP_PROJECT_CSV_READER_H

#include <fstream>
#include <string>


class CSVReader {

private:
    std::ifstream file;
    int current_line_count=0;

    static int totalLines();

public:
    int total_lines=0;
    std::string current_line;
    bool continue_reading;
    std::string full_path;

    CSVReader(std::string path, std::string filename);
    std::vector<std::string> readLine();
    void close();

//    void GoToRow(int row_number);
};

#endif //CPP_PROJECT_CSV_READER_H
