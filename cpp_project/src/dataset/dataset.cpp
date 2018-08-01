
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
    array_index = 0;
}

void Dataset::setColumn(int column_index){
    array_index = 0;
    if (column_index != 0){
        array_index = column_index % (column_code_vector.size() - 1);
        if (array_index == 0){ array_index = column_code_vector.size() - 1; }
    }
    column_code = column_code_vector[array_index];
}

void Dataset::setMaskMode(bool mask_mode_){
    mask_mode = mask_mode_;
}

void Dataset::addBits(int bits){
    if (mask_mode){
        std::cout << "MASK MODE";
    }
    column_code_vector[array_index].addBits(bits, mask_mode);
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

void Dataset::printBits(){
    for(int i=0; i<column_code_vector.size(); i++){
        if (i > 0){
            std::cout << "total_mask_bits " << column_code_vector[i].total_mask_bits << std::endl;
        }
        std::cout << "total_bits " << column_code_vector[i].total_bits << std::endl;
    }
}

//void Dataset::printRange(){
//    column_code.range.print();
//}