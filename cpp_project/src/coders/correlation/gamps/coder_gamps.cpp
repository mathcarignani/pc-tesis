

#include "coder_gamps.h"
#include "mask_coder.h"
#include "time_delta_coder.h"
#include "math_utils.h"
#include "assert.h"
#include "vector_utils.h"

void CoderGAMPS::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    max_window_size_bit_length = MathUtils::bitLength(max_window_size);
}

void CoderGAMPS::codeDataRows(){
    codeTimeDeltaColumn();
    codeColumnGroups();
}

void CoderGAMPS::codeTimeDeltaColumn(){
    column_index = 0;
#if COUT
    std::cout << "ccode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    time_delta_vector = TimeDeltaCoder::code(this);
}

void CoderGAMPS::codeColumnGroups(){
    int total_groups = dataset->column_code_vector.size() - 1; // -1 because of the time delta column
    assert(total_groups > 0);
    for(int i=0; i < total_groups; i++){
    #if COUT
        std::cout << "ccode column group = " << i << std::endl;
    #endif
        codeColumnGroup(i, total_groups);
    }
}

void CoderGAMPS::codeColumnGroup(int group_index, int total_groups){
    int base_threshold, ratio_threshold;
    std::vector<int> column_group_indexes = calculateGroupParams(group_index, total_groups, base_threshold, ratio_threshold);

    std::cout << "base_threshold = " << base_threshold << std::endl;
    std::cout << "ratio_threshold = " << ratio_threshold << std::endl;

    std::vector<std::string> base_column;

    for(int i=0; i < column_group_indexes.size(); i++){
    #if COUT
        std::cout << "ccode column_index " << column_group_indexes.at(i) << std::endl;
    #endif
        if (i == 0){ // code base signal
            base_column = codeBaseColumn(base_threshold);
        }
        else { // code ratio signal
            codeRatioColumn(ratio_threshold, base_column);
        }
    }
}

std::vector<int> CoderGAMPS::calculateGroupParams(int group_index, int total_groups, int & base_threshold, int & ratio_threshold){
    std::vector<int> column_group_indexes; // vector with the indexes of all the columns in the group
    int max_threshold = 0;
    for(int i=group_index + 1; i <= dataset->data_columns_count; i+=total_groups){
        std::cout << "i = " << i << std::endl;
        column_group_indexes.push_back(i);
        int i_threshold = error_thresholds_vector.at(i);
        max_threshold = (i_threshold > max_threshold ? i_threshold : max_threshold);
    }
    VectorUtils::printIntVector(column_group_indexes);
    VectorUtils::printIntVector(error_thresholds_vector);
    std::cout << "max_threshold = " << max_threshold << std::endl;

    // calculate base_threshold and ratio_threshold
    base_threshold = max_threshold / 2;
    ratio_threshold = base_threshold;
    if (base_threshold + ratio_threshold < max_threshold) { base_threshold++; }
    assert(base_threshold + ratio_threshold == max_threshold);
    return column_group_indexes;
}

#endif // MASK_MODE
