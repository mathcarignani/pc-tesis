
#ifndef CPP_PROJECT_STRUCTS_H
#define CPP_PROJECT_STRUCTS_H

struct MapEntry {
    // If mi == i: * signal i indicates the base signal
    //             * ratio_signals is a vector with the indexes of all the ratio signals
    // Otherwise: * i is compressed with respect to signal m
    //            * ratio_signals is an empty vector
    int column_index;
    int base_column_index;
    std::vector<int> ratio_signals;

    MapEntry(int column_index_, int base_column_index_, std::vector<int> ratio_signals_){
        column_index = column_index_;
        base_column_index = base_column_index_;
        ratio_signals = ratio_signals_;
    }
};

struct MappingTable {
    std::vector<MapEntry*> mapping_vector;
    std::vector<int> base_columns_indexes;

    MappingTable(std::vector<MapEntry*> mapping_vector_, std::vector<int> base_columns_indexes_){
        mapping_vector = mapping_vector_;
        base_columns_indexes = base_columns_indexes_;
    }

    std::vector<int> ratioSignals(int base_column_index){
        return mapping_vector.at(base_column_index - 1)->ratio_signals;
    }

    int baseColumnsCount(){
        return base_columns_indexes.size();
    }
};

#endif //CPP_PROJECT_STRUCTS_H
