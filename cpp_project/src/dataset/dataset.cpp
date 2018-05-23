
#include "dataset.h"

#include "assert.h"

Dataset::Dataset(){

}

Dataset::Dataset(std::vector<Range> ranges, std::vector<int> bits, int data_columns_count_){
    assert(ranges.size() > 0);
    assert(ranges.size() == bits.size());
    assert(ranges.size() <= data_columns_count_ + 1);

    for(int i=0; i < ranges.size(); i++){
        ColumnCode new_column_code = ColumnCode(ranges[i], bits[i]);
        column_code_vector.emplace_back(new_column_code);
    }
    column_code = column_code_vector[0];
    data_columns_count = data_columns_count_;
}

void Dataset::setColumn(int column_index){
    int array_index = 0;
    if (column_index != 0){
        array_index = column_index % (column_code_vector.size() - 1);
        if (array_index == 0){ array_index = column_code_vector.size() - 1; }
    }
    column_code = column_code_vector[array_index];
}

void Dataset::addBits(int bits){
    column_code.addBits(bits);
}

int Dataset::getBits(){
    addBits(column_code.bits);
    return column_code.bits;
}

int Dataset::bits(){
    return column_code.bits;
}

int Dataset::offset(){
    return column_code.offset;
}

int Dataset::nan(){
    return column_code.nan;
}

bool Dataset::insideRange(int value){
    return column_code.range.insideRange(value);
}

//void Dataset::printRange(){
//    column_code.range.print();
//}