
#ifndef CPP_PROJECT_INPUT_H
#define CPP_PROJECT_INPUT_H

#include "csv_reader.h"

class CoderInput {

private:
    CSVReader* input_csv;

public:
    int total_data_rows;
    int total_rows;
    int column_index;

    CoderInput(CSVReader* input_csv_, int column_index_);
    int getByte();
    int getValue();
};

#endif //CPP_PROJECT_INPUT_H
