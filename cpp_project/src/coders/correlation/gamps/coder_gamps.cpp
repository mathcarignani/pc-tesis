
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
    codeCoderParameters(Constants::CODER_GAMPS, window_size);
}

void CoderGAMPS::codeDataRows(){
    codeTimeDeltaColumn();
    codeMapping();
    codeColumnGroups();
}

void CoderGAMPS::codeTimeDeltaColumn(){
    column_index = 0;
#if COUT
    std::cout << "ccode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    dataset->setMode("DATA");
    time_delta_vector = TimeDeltaCoder::code(this);
}

//
// TODO: implement this method
//
void CoderGAMPS::calculateMappingTable(){
    int base_columns_count = dataset->dataColumnsGroupCount();
    std::vector<MapEntry*> mapping_vector;
    std::vector<int> base_columns_indexes;
    MapEntry* map_entry;

    for(int i = 0; i < dataset->data_columns_count; i++){
        std::vector<int> ratio_signals;
        int column_index = i + 1;
        if (i < base_columns_count){ // base column
            base_columns_indexes.push_back(column_index);
            for (int j = i + base_columns_count; j < dataset->data_columns_count; j += base_columns_count){
                ratio_signals.push_back(j + 1);
            }
            map_entry = new MapEntry(column_index, column_index, ratio_signals);
        }
        else { // ratio column
            int base_column_index = (i % base_columns_count) + 1;
            map_entry = new MapEntry(column_index, base_column_index, ratio_signals);
        }
        mapping_vector.push_back(map_entry);
    }
    mapping_table = new MappingTable(base_columns_indexes, mapping_vector);
    mapping_table->print();
}

void CoderGAMPS::codeMapping(){
    calculateMappingTable();
    std::vector<int> base_column_index_vector = mapping_table->baseColumnIndexVector();
    int vector_to_code_size = base_column_index_vector.size();
#if CHECKS
    assert(vector_to_code_size == dataset->data_columns_count);
#endif
    int column_index_bit_length = MathUtils::bitLength(vector_to_code_size);
    for (int i = 0; i < vector_to_code_size; i++){
        codeInt(base_column_index_vector.at(i) - 1, column_index_bit_length);
    }
}

void CoderGAMPS::codeColumnGroups(){
#if CHECKS
    assert(error_thresholds_vector.size() - 1 == mapping_table->baseColumnsCount());
#endif
    for(int i=0; i < mapping_table->baseColumnsCount(); i++){
        int base_column_index = mapping_table->base_columns_indexes.at(i);
        codeColumnGroup(base_column_index);
    }
}

void CoderGAMPS::codeColumnGroup(int base_column_index){
    int base_threshold, ratio_threshold;
    groupThresholds(error_thresholds_vector.at(base_column_index), base_threshold, ratio_threshold);
    std::cout << "base_threshold = " << base_threshold << std::endl;
    std::cout << "ratio_threshold = " << ratio_threshold << std::endl;

    // code base column
    column_index = base_column_index;
#if COUT
    std::cout << "ccode base column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    std::vector<std::string> base_column = codeBaseColumn(base_threshold);
    dataset->updateRangesGAMPS(base_column_index);

    // code ratio columns
    std::vector<int> column_group_indexes = mapping_table->ratioSignals(base_column_index);
    for(int i=0; i < column_group_indexes.size(); i++){
        column_index = column_group_indexes.at(i);
    #if COUT
        std::cout << "ccode ratio column_index " << column_index << std::endl;
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
    dataset->setMode("MASK");
    total_data_rows = MaskCoder::code(this, column_index);
#endif
    std::vector<std::string> column;

    dataset->setMode("DATA");
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
    dataset->setMode("MASK");
    total_data_rows = MaskCoder::code(this, column_index);
#endif
    dataset->setMode("DATA");
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
    int diff = StringUtils::stringToInt(ratio_value) - StringUtils::stringToInt(base_value); // TODO: wrong! use division
    return StringUtils::intToString(diff);
}
