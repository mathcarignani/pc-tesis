
#include "dataset.h"
#include "assert.h"


Dataset::Dataset(std::vector<Range> ranges, int data_columns_count_){
    assert(ranges.size() > 0);
    assert(ranges.size() <= data_columns_count_ + 1);

    for(int i=0; i < ranges.size(); i++){
        ColumnCode* new_column_code = new ColumnCode(ranges[i], i);
        column_code_vector.emplace_back(new_column_code);
    }
    column_code = column_code_vector[0];
    data_columns_count = data_columns_count_;
    array_index = 0;
}

void Dataset::updateRangesGAMPS(){
    for(int i=1; i < column_code_vector.size(); i++){
        ColumnCode* current_column_code = column_code_vector.at(i);
        int nan_minus_one = current_column_code->nan - 1;
        Range range = Range(-nan_minus_one, nan_minus_one);
        current_column_code->updateRange(range, i);
    }
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
    column_code_vector[array_index]->addBits(bits, mask_mode);
}

int Dataset::getBits(){
    addBits(column_code->bits);
    return column_code->bits;
}

int Dataset::bits(){
    return column_code->bits;
}

int Dataset::offset(){
    return column_code->offset;
}

int Dataset::nan(){
    return column_code->nan;
}

bool Dataset::insideRange(int value){
    return column_code->range.insideRange(value);
}

void Dataset::printBits(){
    for(int i=0; i<column_code_vector.size(); i++){
        std::cout << "total_mask_bits " << column_code_vector[i]->total_mask_bits << std::endl;
        std::cout << "total_bits " << column_code_vector[i]->total_bits << std::endl;
    }
}

std::vector<int> Dataset::totalMaskBitsArray(){
    int size = column_code_vector.size();
    std::vector<int> res(size);
    for(int i=0; i < size; i++){
        res[i] = column_code_vector[i]->total_mask_bits;
    }
    return res;
}

std::vector<int> Dataset::totalBitsArray(){
    int size = column_code_vector.size();
    std::vector<int> res(size);
    for(int i=0; i < size; i++){
        res[i] = column_code_vector[i]->total_bits;
    }
    return res;
}

//void Dataset::printRange(){
//    column_code.range.print();
//}