
#include "dataset.h"

#include "assert.h"

Dataset::Dataset(){

}

Dataset::Dataset(std::vector<Range> ranges, std::vector<int> bits){
    assert(ranges.size() > 0);
    assert(ranges.size() == bits.size());

    for(int i=0; i < ranges.size(); i++){
        ColumnCode new_column_code = ColumnCode(ranges[i], bits[i]);
        column_code_vector.emplace_back(new_column_code);
    }
    column_code = column_code_vector[0];
}

void Dataset::setColumn(int column_index){
    assert(column_index < column_code_vector.size());

    column_code = column_code_vector[column_index];
}

void Dataset::addBits(int bits){
    column_code.addBits(bits);
}
