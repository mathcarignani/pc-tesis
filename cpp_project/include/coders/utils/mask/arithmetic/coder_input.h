
#ifndef CPP_PROJECT_INPUT_H
#define CPP_PROJECT_INPUT_H

#include "csv_reader.h"

class CoderInput {

private:
    CSVReader* input_csv;

public:
    int total_data_rows;

    CoderInput(CSVReader* input_csv_, int column_index);
    int getByte();
};

#endif //CPP_PROJECT_INPUT_H
