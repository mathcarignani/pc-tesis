
#ifndef CPP_PROJECT_CSV_READER_H
#define CPP_PROJECT_CSV_READER_H

#include <fstream>
#include <string>
#include "text_reader.h"
#include "path.h"
#include <vector>


class CSVReader: public TextReader {

private:
    void constructor(std::string path, std::string filename);
    int column_index;

public:
    CSVReader(Path path);

    // PRE: continue_reading
    std::vector<std::string> readLineCSV();
    // PRE: continue reading
    std::string readLineCSVWithIndex();

    void goToFirstDataRow(int column_index_);
};

#endif //CPP_PROJECT_CSV_READER_H
