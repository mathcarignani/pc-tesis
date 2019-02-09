
#include "coder_gamps.h"
#include "mask_coder.h"
#include "time_delta_coder.h"
#include "math_utils.h"
#include "assert.h"
#include "vector_utils.h"
#include "coder_apca.h"
#include "gamps_utils.h"

#include "GAMPS.h"
#include "GAMPSInput.h"

void CoderGAMPS::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderGAMPS::codeCoderParams(){
    codeCoderParameters(Constants::CODER_GAMPS, window_size);
}

void CoderGAMPS::codeDataRows(){
    codeTimeDeltaColumn();
    GAMPSOutput* gamps_output = getGAMPSOutput();
    calculateMappingTable(gamps_output);
    codeMapping();
    codeColumnGroups(gamps_output);
}

GAMPSOutput* CoderGAMPS::getGAMPSOutput(){
    double epsilon = 1;
    GAMPSInput* gamps_input = getGAMPSInput();
    GAMPS* gamps = new GAMPS(epsilon, gamps_input);
    gamps->compute();
    return gamps->getOutput();
}

GAMPSInput* CoderGAMPS::getGAMPSInput(){
    CMultiDataStream* multiStream = new CMultiDataStream(dataset->data_columns_count);
    for(int i = 0; i < dataset->data_columns_count; i++)
    {
        int col_index = i + 1;
        std::cout << "Parsing column " << col_index << std::endl;

        CDataStream* signal = getColumn(col_index);
        multiStream->addSingleStream(signal);
    }
    GAMPSInput* gamps_input = new GAMPSInput(multiStream);
    return gamps_input;
}

void CoderGAMPS::calculateMappingTable(GAMPSOutput* gamps_output){
    std::vector<int> base_column_index_vector;
    for (int i = 0; i < dataset->data_columns_count; i++){
        int val = gamps_output->getTgood()[i];
        int base_column_index = val + 1;
        base_column_index_vector.push_back(base_column_index);
    }
    mapping_table = new MappingTable(base_column_index_vector);
    mapping_table->print();
}

CDataStream* CoderGAMPS::getColumn(int column_index){
    CDataStream* dataStream = new CDataStream();

    std::string previous_csv_value = "1";

    input_csv->goToFirstDataRow(column_index);
    int timestamp = 0;

    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();

        if (Constants::isNoData(csv_value)){
            csv_value = previous_csv_value;
        }

        DataItem entry;
        int value = StringUtils::stringToInt(csv_value);
        assert(value > 0);
        entry.value = value;
        entry.timestamp = timestamp;
        dataStream->add(entry);
        timestamp++;
    }
    assert(dataStream->size() == data_rows_count);
    assert(timestamp == data_rows_count);
    return dataStream;
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

void CoderGAMPS::codeMapping(){
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

void CoderGAMPS::codeColumnGroups(GAMPSOutput* gamps_output){
    int base_count = 0;
    int ratio_count = 0;

    DynArray<GAMPSEntry>* array;

    for(int i = 0; i < dataset->data_columns_count; i++){
        if(gamps_output->getTgood()[i] == i){ // base signal
            std::cout << "code base signal i = " << i + 1 << std::endl;
            DynArray<GAMPSEntry>** temp = gamps_output->getResultBaseSignal();
            array = temp[base_count++];
        }
        else{ // ratio signal
            std::cout << "code ratio signal i = " << i + 1 << std::endl;
            DynArray<GAMPSEntry>** temp = gamps_output->getResultRatioSignal();
            array = temp[ratio_count++];
        }
        codeColumn(array);
    }
}

void CoderGAMPS::codeColumn(DynArray<GAMPSEntry>* array){
    std::cout << "array->size() = " << array->size() << std::endl;
    for(int i=0; i < array->size(); i++){
        GAMPSEntry entry = array->getAt(i);
        std::cout << "entry.value = " << entry.value << std::endl;
        std::cout << "entry.endingTimestamp = " << entry.endingTimestamp << std::endl;

        codeDouble(entry.value);
        codeDouble(entry.endingTimestamp);
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//
// TODO: implement this method
//
//void CoderGAMPS::calculateMappingTable(){
//    int base_columns_count = dataset->dataColumnsGroupCount();
//    std::vector<MapEntry*> mapping_vector;
//    std::vector<int> base_columns_indexes;
//    MapEntry* map_entry;
//
//    for(int i = 0; i < dataset->data_columns_count; i++){
//        std::vector<int> ratio_signals;
//        int column_index = i + 1;
//        if (i < base_columns_count){ // base column
//            base_columns_indexes.push_back(column_index);
//            for (int j = i + base_columns_count; j < dataset->data_columns_count; j += base_columns_count){
//                ratio_signals.push_back(j + 1);
//            }
//            map_entry = new MapEntry(column_index, column_index, ratio_signals);
//        }
//        else { // ratio column
//            int base_column_index = (i % base_columns_count) + 1;
//            map_entry = new MapEntry(column_index, base_column_index, ratio_signals);
//        }
//        mapping_vector.push_back(map_entry);
//    }
//    mapping_table = new MappingTable(base_columns_indexes, mapping_vector);
//    mapping_table->print();
//}

//void CoderGAMPS::codeColumnGroups(){
//#if CHECKS
//    assert(error_thresholds_vector.size() - 1 == mapping_table->baseColumnsCount());
//#endif
//    for(int i=0; i < mapping_table->baseColumnsCount(); i++){
//        int base_column_index = mapping_table->base_columns_indexes.at(i);
//        codeColumnGroup(base_column_index);
//    }
//}

//void CoderGAMPS::codeColumnGroup(int base_column_index){
//    int base_threshold, ratio_threshold;
//    groupThresholds(error_thresholds_vector.at(base_column_index), base_threshold, ratio_threshold);
//    std::cout << "base_threshold = " << base_threshold << std::endl;
//    std::cout << "ratio_threshold = " << ratio_threshold << std::endl;
//
//    // code base column
//    column_index = base_column_index;
//#if COUT
//    std::cout << "ccode base column_index " << column_index << std::endl;
//#endif
//    dataset->setColumn(column_index);
//    std::vector<std::string> base_column = codeBaseColumn(base_threshold);
//    dataset->updateRangesGAMPS(base_column_index);
//
//    // code ratio columns
//    std::vector<int> column_group_indexes = mapping_table->ratioSignals(base_column_index);
//    for(int i=0; i < column_group_indexes.size(); i++){
//        column_index = column_group_indexes.at(i);
//    #if COUT
//        std::cout << "ccode ratio column_index " << column_index << std::endl;
//    #endif
//        dataset->setColumn(column_index);
//        codeRatioColumn(ratio_threshold, base_column);
//    }
//}

//void CoderGAMPS::groupThresholds(int threshold, int & base_threshold, int & ratio_threshold){
//    base_threshold = threshold / 2;
//    ratio_threshold = base_threshold;
//    if (base_threshold + ratio_threshold < threshold) { base_threshold++; }
//    assert(base_threshold + ratio_threshold == threshold);
//}

//std::vector<std::string> CoderGAMPS::codeBaseColumn(int error_threshold){
//#if MASK_MODE
//    dataset->setMode("MASK");
//    total_data_rows = MaskCoder::code(this, column_index);
//#endif
//    std::vector<std::string> column;
//
//    dataset->setMode("DATA");
//    window = new APCAWindow(window_size, error_threshold);
//
//    row_index = -1;
//    input_csv->goToFirstDataRow(column_index);
//    while (input_csv->continue_reading){
//        row_index++;
//        std::string csv_value = input_csv->readNextValue();
//        column.push_back(csv_value);
//        CoderAPCA::codeColumnWhile(this, window, csv_value);
//    }
//    CoderAPCA::codeColumnAfter(this, window);
//    return column;
//}

//void CoderGAMPS::codeRatioColumn(int error_threshold, std::vector<std::string> base_column){
//#if MASK_MODE
//    dataset->setMode("MASK");
//    total_data_rows = MaskCoder::code(this, column_index);
//#endif
//    dataset->setMode("DATA");
//    window = new APCAWindow(window_size, error_threshold);
//
//    row_index = -1;
//    input_csv->goToFirstDataRow(column_index);
//    while (input_csv->continue_reading){
//        row_index++;
//        std::string ratio_value = input_csv->readNextValue();
//        std::string base_value = base_column.at(row_index);
//
//        std::string diff_value = calculateDiff(base_value, ratio_value);
//        CoderAPCA::codeColumnWhile(this, window, diff_value);
//    }
//    CoderAPCA::codeColumnAfter(this, window);
//}

//std::string CoderGAMPS::calculateDiff(std::string base_value, std::string ratio_value){
//    if (Constants::isNoData(base_value) || Constants::isNoData(ratio_value)) {
//        return ratio_value;
//    }
//    int int_ratio_value = StringUtils::stringToInt(ratio_value);
//    int int_base_value = StringUtils::stringToInt(base_value);
//
//    std::string diff = calculateDeltaSignal(int_ratio_value, int_base_value);
////    std::string diff = calculateRatioSignal(int_ratio_value, int_base_value);
//
//    return diff;
//}

//std::string CoderGAMPS::calculateDeltaSignal(int vi_t, int vj_t){
//    int delta = vi_t - vj_t;
//    return StringUtils::intToString(delta);
//}
//
//std::string CoderGAMPS::calculateRatioSignal(int vi_t, int vj_t){
//    assert(vi_t > 0);
//    assert(vj_t > 0);
//    double ratio = (double) vi_t / vj_t;
//    return StringUtils::doubleToString(ratio);
//}
