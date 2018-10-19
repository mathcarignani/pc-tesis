
#include "gamps_utils.h"

std::vector<int> GAMPSUtils::columnGroupIndexes(Dataset* dataset, int group_index){
    std::vector<int> column_group_indexes; // vector with the indexes of all the columns in the group
    for(int i=group_index + 1; i <= dataset->data_columns_count; i+=dataset->dataColumnsGroupCount()){
        column_group_indexes.push_back(i);
    }
    return column_group_indexes;
}
