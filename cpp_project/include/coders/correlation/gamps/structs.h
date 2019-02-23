
#ifndef CPP_PROJECT_STRUCTS_H
#define CPP_PROJECT_STRUCTS_H

#include "vector_utils.h"
#include "GAMPSOutput.h"

class MapEntry {
public:
    // index of the column in the dataset file
    // column_index >= 1 since the delta time column is ignored
    int column_index;

    // if base_column_index == 0 then the MapEntry corresponds to a nodata column
    // else if base_column_index == column_index then the MapEntry corresponds to a base column
    // else the MapEntry corresponds to a ratio column and base_column_index is the index of its base column
    int base_column_index;

    // if base_column_index == column_index then this vector has the indexes of all its ratio columns
    // else this vector is empty
    std::vector<int> ratio_columns;

    MapEntry(int column_index_, int base_column_index_, std::vector<int> ratio_columns_);
    bool isNodataEntry();
    bool isBaseColumn();
    bool isRatioColumn();
    void print();
};

class MappingTable {
private:
    std::vector<int> getRatioColumns(std::vector<int> base_column_index_vector, int column_index);

public:
    std::vector<int> base_columns_indexes;
    std::vector<int> nodata_columns_indexes;
    std::vector<MapEntry*> mapping_vector;
    int data_columns_count; // number of data columns (some of them can be nodata)
    int gamps_columns_count; // number of data columns which contain at least an integer value, used in the GAMPS algorithm

    // Only called in CoderGAMPS
    MappingTable();
    void setNoDataColumnsIndexes(std::vector<bool> nodata_columns, int data_columns_count_);
    void calculate(GAMPSOutput* gamps_output);
    int getColumnIndex(int gamps_col_index);
    int getRatioGampsColumnIndex(int column_index);

    // Only called in DecoderGAMPS
    MappingTable(std::vector<int> vector);


    void createBaseColumnIndex();

    int ratioColumnsIndexesAt(int index);

    bool isNodataColumnIndex(int col_index);

    std::vector<int> ratioColumns(int base_column_index);
    std::vector<int> baseColumnIndexVector();
    bool isBaseColumn(int column_index);
    void print();
};

#endif //CPP_PROJECT_STRUCTS_H
