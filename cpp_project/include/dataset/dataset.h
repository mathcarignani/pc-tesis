
#ifndef CPP_PROJECT_DATASET_H
#define CPP_PROJECT_DATASET_H

#include "column_code.h"

struct Dataset {

private:
    std::vector<ColumnCode> column_code_vector;
    ColumnCode column_code;

public:
    Dataset();
    Dataset(std::vector<Range> ranges, std::vector<int> bits);
    void setColumn(int column_index);
    void addBits(int bits);
};

#endif //CPP_PROJECT_DATASET_H
