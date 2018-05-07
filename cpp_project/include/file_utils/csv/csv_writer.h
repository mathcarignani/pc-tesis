
#ifndef CPP_PROJECT_CSV_WRITER_H
#define CPP_PROJECT_CSV_WRITER_H

#include <fstream>
#include <string>
#include <vector>

class CSVWriter {

private:
    std::ofstream file;

public:
    std::string full_path;

    CSVWriter(std::string path, std::string filename);

    void writeRow(std::vector<std::string> row);

    void close();
};

#endif //CPP_PROJECT_CSV_WRITER_H
