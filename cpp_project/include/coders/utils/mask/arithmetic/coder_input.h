
#ifndef CPP_PROJECT_INPUT_H
#define CPP_PROJECT_INPUT_H

#include "csv_reader.h"
#include "coder_common.h"

class CoderInput {

private:
    CoderCommon* coder;
    CSVReader* input_csv;
    Dataset* dataset;
    int last_column_index; // index of the last masked column
    int column_index;

    void setNextColumn(int col_index);
    void endCurrentColumn();

public:
    int total_data_rows;
    int total_rows;
    std::vector<int> total_data_rows_vector;

    // variables used by compressor.h
    bool reset_model;
    bool eof;

    CoderInput(CoderCommon* coder_, int first_column_index_, int last_column_index_);
    int getByte(); // PRE: !eof()

};

#endif //CPP_PROJECT_INPUT_H
