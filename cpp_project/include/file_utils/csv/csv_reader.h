
#ifndef CPP_PROJECT_CSV_READER_H
#define CPP_PROJECT_CSV_READER_H

#include <fstream>
#include <string>
#include "text_reader.h"


class CSVReader: public TextReader {

public:
    CSVReader(std::string path, std::string filename);
    // PRE: continue_reading
    std::vector<std::string> readLineCSV();
};

#endif //CPP_PROJECT_CSV_READER_H
