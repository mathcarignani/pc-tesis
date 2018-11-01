
#include "coder_gamps.h"
#include "mask_coder.h"
#include "time_delta_coder.h"
#include "math_utils.h"
#include "assert.h"
#include "vector_utils.h"
#include "coder_apca.h"
#include "gamps_utils.h"

void CoderGAMPS::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    window_size_bit_length = MathUtils::bitLength(window_size);
}

void CoderGAMPS::codeCoderParams(){
    codeCoderParameters(30, window_size);
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
    assert(error_thresholds_vector.size() == dataset->dataColumnsGroupCount() + 1);
    for(int i=0; i < dataset->dataColumnsGroupCount(); i++){
    #if COUT
        std::cout << "ccode column group = " << i << std::endl;
    #endif
        codeColumnGroup(i);
    }
}

void CoderGAMPS::codeColumnGroup(int group_index){
    std::vector<int> column_group_indexes = GAMPSUtils::columnGroupIndexes(dataset, group_index);
    VectorUtils::printIntVector(column_group_indexes);

    int base_threshold, ratio_threshold;
    groupThresholds(error_thresholds_vector.at(group_index + 1), base_threshold, ratio_threshold);
    std::cout << "base_threshold = " << base_threshold << std::endl;
    std::cout << "ratio_threshold = " << ratio_threshold << std::endl;

    // code base column
    column_index = column_group_indexes.at(0);
#if COUT
    std::cout << "ccode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    std::vector<std::string> base_column = codeBaseColumn(base_threshold);
    dataset->updateRangesGAMPS(group_index);

    // code ratio columns
    for(int i=1; i < column_group_indexes.size(); i++){
        column_index = column_group_indexes.at(i);
    #if COUT
        std::cout << "ccode column_index " << column_index << std::endl;
    #endif
        dataset->setColumn(column_index);
        codeRatioColumn(ratio_threshold, base_column);
    }
}

void CoderGAMPS::groupThresholds(int threshold, int & base_threshold, int & ratio_threshold){
    base_threshold = threshold / 2;
    ratio_threshold = base_threshold;
    if (base_threshold + ratio_threshold < threshold) { base_threshold++; }
    assert(base_threshold + ratio_threshold == threshold);
}

std::vector<std::string> CoderGAMPS::codeBaseColumn(int error_threshold){
#if MASK_MODE
    total_data_rows = MaskCoder::code(this, column_index);
#endif
    std::vector<std::string> column;

    dataset->setMaskMode(false);
    window = new APCAWindow(window_size, error_threshold);

    row_index = -1;
    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading){
        row_index++;
        std::string csv_value = input_csv->readLineCSVWithIndex();
        column.push_back(csv_value);
        CoderAPCA::codeColumnWhile(this, window, csv_value);
    }
    CoderAPCA::codeColumnAfter(this, window);
    return column;
}

void CoderGAMPS::codeRatioColumn(int error_threshold, std::vector<std::string> base_column){
#if MASK_MODE
    total_data_rows = MaskCoder::code(this, column_index);
#endif
    dataset->setMaskMode(false);
    window = new APCAWindow(window_size, error_threshold);

    row_index = -1;
    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading){
        row_index++;
        std::string csv_value = input_csv->readLineCSVWithIndex();
        std::string diff_value = calculateDiff(base_column.at(row_index), csv_value);
        CoderAPCA::codeColumnWhile(this, window, diff_value);
    }
    CoderAPCA::codeColumnAfter(this, window);
}

std::string CoderGAMPS::calculateDiff(std::string base_value, std::string ratio_value){
    if (Constants::isNoData(base_value) || Constants::isNoData(ratio_value)) { return ratio_value; }

    int diff = StringUtils::stringToInt(ratio_value) - StringUtils::stringToInt(base_value);
    // std::cout << "ratio_value = " << StringUtils::stringToInt(ratio_value) << " | base_value = " << StringUtils::stringToInt(base_value) << " | diff = " << diff << std::endl;
    return StringUtils::intToString(diff);
}
