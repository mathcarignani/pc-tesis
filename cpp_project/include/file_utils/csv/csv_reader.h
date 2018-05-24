
#ifndef CPP_PROJECT_CSV_READER_H
#define CPP_PROJECT_CSV_READER_H

#include <fstream>
#include <string>
#include "text_reader.h"
#include "path.h"


class CSVReader: public TextReader {

private:
    void constructor(std::string path, std::string filename);

public:
    CSVReader();
    CSVReader(std::string path, std::string filename);
    CSVReader(Path path);

    // PRE: continue_reading
    std::vector<std::string> readLineCSV();
    // PRE: continue reading
    std::string readLineCSVWithIndex(int index);
};

#endif //CPP_PROJECT_CSV_READER_H
