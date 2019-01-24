
#ifndef CPP_PROJECT_STRUCTS_H
#define CPP_PROJECT_STRUCTS_H

#include "vector_utils.h"

class MapEntry {
public:
    // If mi == i: * signal i indicates the base signal
    //             * ratio_signals is a vector with the indexes of all the ratio signals
    // Otherwise: * i is compressed with respect to signal m
    //            * ratio_signals is an empty vector
    int column_index;
    int base_column_index;
    std::vector<int> ratio_signals;

    MapEntry(int column_index_, int base_column_index_, std::vector<int> ratio_signals_);
    void print();
};

class MappingTable {
public:
    std::vector<int> base_columns_indexes;
    std::vector<MapEntry*> mapping_vector;

    MappingTable(std::vector<int> base_columns_indexes_, std::vector<MapEntry*> mapping_vector_);
    MappingTable(std::vector<int> base_column_index_vector);
    std::vector<int> ratioSignals(int base_column_index);
    std::vector<int> baseColumnIndexVector();
    int baseColumnsCount();
    void print();
};

#endif //CPP_PROJECT_STRUCTS_H
