
#include "structs.h"

MapEntry::MapEntry(int column_index_, int base_column_index_, std::vector<int> ratio_columns_){
    column_index = column_index_;
    base_column_index = base_column_index_;
    ratio_columns = ratio_columns_;
}

void MapEntry::print(){
    std::cout << "column_index = " << column_index;
    if (base_column_index == 0) {
        std::cout << " [nodata column]" << std::endl;
        return;
    }
    std::cout << ", base_column_index = " << base_column_index;
    if (ratio_columns.size() > 0){
        std::cout << ", ratio_columns = "; VectorUtils::printIntVector(ratio_columns);
    }
    else{
        std::cout << std::endl;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

MappingTable::MappingTable(){}


MappingTable::MappingTable(std::vector<int> base_columns_indexes_, std::vector<MapEntry*> mapping_vector_){
    base_columns_indexes = base_columns_indexes_;
    mapping_vector = mapping_vector_;
}

std::vector<int> MappingTable::getRatioColumns(std::vector<int> base_column_index_vector, int column_index){
    std::vector<int> ratio_signals;
    for (int j = 0; j < base_column_index_vector.size(); j++){
        int column_index_j = j + 1;
        int base_column_index_j = base_column_index_vector.at(j);
        if (base_column_index_j == column_index && base_column_index_j != column_index_j){
            ratio_signals.push_back(column_index_j);
        }
    }
    return ratio_signals;
}

void MappingTable::addNodataColumnIndex(int col_index){
    nodata_columns_indexes.push_back(col_index);
}

bool MappingTable::isNodataColumnIndex(int col_index){
    return VectorUtils::vectorIncludesInt(nodata_columns_indexes, col_index);
}

void MappingTable::calculate(int data_columns_count, GAMPSOutput* gamps_output){
    int gamps_output_count = data_columns_count - nodata_columns_indexes.size();
    assert(gamps_output_count > 0);
    int data_column_index = 0;
    for(int i=1; i <= data_columns_count; i++){
        std::vector<int> ratio_signals;
        MapEntry* map_entry;

        if (VectorUtils::vectorIncludesInt(nodata_columns_indexes, i)){
            map_entry = new MapEntry(i, 0, ratio_signals);
        }
        else {
            int base_index = gamps_output->getTgood()[data_column_index];
            int base_index_mapped = getColumnIndex(data_columns_count, base_index);

            // add ratio signals
            for(int j=0; j < gamps_output_count; j++){
                int base_j = gamps_output->getTgood()[j];
                int j_index = getColumnIndex(data_columns_count, j);
                if (base_j != j && base_j == data_column_index){
                    ratio_signals.push_back(j_index);
                    addBaseColumnIndex(base_index_mapped);
                }
            }
            map_entry = new MapEntry(i, base_index_mapped, ratio_signals);
            data_column_index++;
        }
        mapping_vector.push_back(map_entry);
    }
}

int MappingTable::getColumnIndex(int data_columns_count, int gamps_col_index){
    int data_column_index = 0;

    int i = 1;
    while (i <= data_columns_count) {
        if (!VectorUtils::vectorIncludesInt(nodata_columns_indexes, i)){
            if (data_column_index == gamps_col_index) { break; }
            data_column_index++;
        }
        i++;
    }
    return i;
}

void MappingTable::addBaseColumnIndex(int base_column_index){
    if (!VectorUtils::vectorIncludesInt(base_columns_indexes, base_column_index)){
        base_columns_indexes.push_back(base_column_index);
    }
}

std::vector<int> MappingTable::ratioColumns(int base_column_index){
    return mapping_vector.at(base_column_index - 1)->ratio_columns;
}

std::vector<int> MappingTable::baseColumnIndexVector(){
    std::vector<int> res;
    for (int i = 0; i < mapping_vector.size(); i++){
        MapEntry* map_entry = mapping_vector.at(i);
        res.push_back(map_entry->base_column_index );
    }
    return res;
}

bool MappingTable::isBaseColumn(int column_index){
    return mapping_vector.at(column_index - 1)->base_column_index == column_index;
}

int MappingTable::baseColumnsCount(){
    return base_columns_indexes.size();
}

void MappingTable::print(){
    std::cout << "------------------------" << std::endl;
    std::cout << "MappingTable" << std::endl;
    std::cout << "nodata_columns_indexes = "; VectorUtils::printIntVector(nodata_columns_indexes);
    std::cout << "base_columns_indexes = "; VectorUtils::printIntVector(base_columns_indexes);
    for(int i=0; i < mapping_vector.size(); i++){
        mapping_vector.at(i)->print();
    }
    std::cout << "------------------------" << std::endl;
}