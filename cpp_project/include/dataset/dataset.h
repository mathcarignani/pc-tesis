
#ifndef CPP_PROJECT_DATASET_H
#define CPP_PROJECT_DATASET_H

#include "column_code.h"

struct Dataset {

private:
    int array_index;
    bool mask_mode;

public:
    ColumnCode* column_code;
    int data_columns_count;
    std::vector<ColumnCode*> column_code_vector;

    Dataset(std::vector<Range> ranges, int data_columns_count_);
    void updateRangesGAMPS();
    void setColumn(int column_index);
    void setMaskMode(bool mask_mode_);
    void addBits(int bits);
    int getBits();
    int bits();
    int offset();
    int nan();
    bool insideRange(int value);
    int dataColumnsGroupCount();
    void printBits();
    std::vector<int> totalMaskBitsArray();
    std::vector<int> totalBitsArray();
//    void printRange();
};

#endif //CPP_PROJECT_DATASET_H
