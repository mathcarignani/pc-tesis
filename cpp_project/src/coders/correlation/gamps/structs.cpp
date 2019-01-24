
#include "structs.h"

MapEntry::MapEntry(int column_index_, int base_column_index_, std::vector<int> ratio_signals_){
    column_index = column_index_;
    base_column_index = base_column_index_;
    ratio_signals = ratio_signals_;
}

void MapEntry::print(){
    std::cout << "column_index = " << column_index << ", base_column_index = " << base_column_index;
    if (ratio_signals.size() > 0){
        std::cout << ", ratio_signals = "; VectorUtils::printIntVector(ratio_signals);
    }
    else{
        std::cout << std::endl;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

MappingTable::MappingTable(std::vector<int> base_columns_indexes_, std::vector<MapEntry*> mapping_vector_){
    base_columns_indexes = base_columns_indexes_;
    mapping_vector = mapping_vector_;
}

MappingTable::MappingTable(std::vector<int> base_column_index_vector){
    for (int i = 0; i < base_column_index_vector.size(); i++){
        int column_index = i + 1;
        int base_column_index = base_column_index_vector.at(i);

        std::vector<int> ratio_signals;
        if (column_index == base_column_index){ // base column, must complete ratio_signals vector
            base_columns_indexes.push_back(column_index);
            for (int j = 0; j < base_column_index_vector.size(); j++){
                int column_index_j = j + 1;
                int base_column_index_j = base_column_index_vector.at(j);
                if (base_column_index_j == column_index && base_column_index_j != column_index_j){
                    ratio_signals.push_back(column_index_j);
                }
            }
        }
        MapEntry* map_entry = new MapEntry(column_index, base_column_index, ratio_signals);
        mapping_vector.push_back(map_entry);
    }
}

std::vector<int> MappingTable::ratioSignals(int base_column_index){
    return mapping_vector.at(base_column_index - 1)->ratio_signals;
}

std::vector<int> MappingTable::baseColumnIndexVector(){
    std::vector<int> res;
    for (int i = 0; i < mapping_vector.size(); i++){
        MapEntry* map_entry = mapping_vector.at(i);
        res.push_back(map_entry->base_column_index );
    }
    return res;
}

int MappingTable::baseColumnsCount(){
    return base_columns_indexes.size();
}

void MappingTable::print(){
    std::cout << "------------" << std::endl;
    std::cout << "MappingTable" << std::endl;
    std::cout << "base_columns_indexes = "; VectorUtils::printIntVector(base_columns_indexes);
    for(int i=0; i < mapping_vector.size(); i++){
        mapping_vector.at(i)->print();
    }
    std::cout << "------------" << std::endl;
}