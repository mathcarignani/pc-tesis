
#include "decoder_gamps.h"
#include "string_utils.h"
#include "math_utils.h"
#include "time_delta_decoder.h"
#include "assert.h"
#include "gamps_utils.h"
#include "vector_utils.h"
#include "mask_decoder.h"
#include "decoder_apca.h"

void DecoderGAMPS::decodeDataRows(){
    int total_columns = dataset->data_columns_count + 1;
    columns = std::vector<std::vector<std::string>> (total_columns);

    decodeTimeDeltaColumn();
    decodeMapping();
    GAMPSOutput* gamps_output = decodeGAMPSOutput();
    decodeColumnGroups(gamps_output);

    transposeMatrix(data_rows_count, columns, total_columns);
}

void DecoderGAMPS::decodeTimeDeltaColumn(){
    int column_index = 0;
#if COUT
    std::cout << "decode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    std::vector<std::string> column = TimeDeltaDecoder::decode(this);
    columns.at(0) = column;
}

void DecoderGAMPS::decodeMapping(){
    int column_index_bit_length = MathUtils::bitLength(dataset->data_columns_count);
    std::vector<int> base_column_index_vector;
    for (int i = 0; i < dataset->data_columns_count; i++){
        int base_column_index = decodeInt(column_index_bit_length) + 1;
        base_column_index_vector.push_back(base_column_index);
    }
//    mapping_table->calculate(dataset->data_columns_count, )
//    mapping_table = new MappingTable(base_column_index_vector);
//    mapping_table->print();
}

GAMPSOutput* DecoderGAMPS::decodeGAMPSOutput(){
    std::cout << "decodeGAMPSOutput" << std::endl;
    GAMPSOutput* gamps_output = new GAMPSOutput(NULL);

    int base_columns_count = mapping_table->baseColumnsCount();
    int ratio_columns_count = dataset->data_columns_count - base_columns_count;

    DynArray<GAMPSEntry>** resultBaseSignal =  new DynArray<GAMPSEntry>*[base_columns_count];
    DynArray<GAMPSEntry>** resultRatioSignal;
    if (ratio_columns_count > 0){
        resultRatioSignal = new DynArray<GAMPSEntry>*[ratio_columns_count];
    }

    int base_count = 0;
    int ratio_count = 0;
    DynArray<GAMPSEntry>* column;

    for (int i = 0; i < dataset->data_columns_count; i++){
        std::cout << "decodeColumn()" << std::endl;
        column = decodeColum();
        if (mapping_table->isBaseColumn(i + 1)){
            std::cout << "decode base signal i = " << i + 1 << std::endl;
            resultBaseSignal[base_count++] = column;
        }
        else {
            std::cout << "decode ratio signal i = " << i + 1 << std::endl;
            resultRatioSignal[ratio_count++] = column;
        }
    }

    gamps_output->setResultBaseSignal(resultBaseSignal);
    gamps_output->setResultRatioSignal(resultRatioSignal);
    return gamps_output;
}

DynArray<GAMPSEntry>* DecoderGAMPS::decodeColum(){
    DynArray<GAMPSEntry>* column = new DynArray<GAMPSEntry>();
    while (true) {
        GAMPSEntry entry;
        entry.value = decodeDouble();
        entry.endingTimestamp = decodeInt();
        column->add(entry);

        std::cout << "entry.value = " << entry.value << std::endl;
        std::cout << "entry.endingTimestamp = " << entry.endingTimestamp << std::endl;

        if (entry.endingTimestamp == time_delta_vector.size()){
            return column;
        }
    }
}

void DecoderGAMPS::decodeColumnGroups(GAMPSOutput* gamps_output){
    std::cout << "decodeColumnGroups" << std::endl;
    int base_count = 0;
    int ratio_count = 0;

    std::vector<std::string> column;
    DynArray<GAMPSEntry>* gamps_column;
    DynArray<GAMPSEntry>** base_signals = gamps_output->getResultBaseSignal();
    DynArray<GAMPSEntry>** ratio_signals = gamps_output->getResultRatioSignal();

    for(int i = 0; i < dataset->data_columns_count; i++){
        int col_index = i + 1;
        if (mapping_table->isBaseColumn(col_index)){
            std::cout << "decode base signal i = " << col_index << std::endl;
            gamps_column = base_signals[base_count++];
            column = getBaseColumn(gamps_column);
        }
        else {
            exit(1);
        }
        columns.at(i + 1) = column;
    }
    std::cout << "END decodeColumnGroups" << std::endl;
}

std::vector<std::string> DecoderGAMPS::getBaseColumn(DynArray<GAMPSEntry>* gamps_column){
    std::vector<std::string> column;

    GAMPSEntry entry;
    int entry_index = 0;
    entry = gamps_column->getAt(entry_index);
    int entry_ending_timestamp = entry.endingTimestamp;
    double entry_value = entry.value;
    int current_timestamp = 0;

    while(current_timestamp < time_delta_vector.size()){
        while (current_timestamp <= entry_ending_timestamp && current_timestamp < time_delta_vector.size()){
            std::string value = StringUtils::doubleToString(entry_value);
            std::cout << "timestamp, value = " << current_timestamp << ", " << value << std::endl;
            column.push_back(value);
            current_timestamp++;
        }
        if (current_timestamp == time_delta_vector.size()){
            break;
        }
        entry_index++;
        entry = gamps_column->getAt(entry_index);
        entry_ending_timestamp = entry.endingTimestamp;
        entry_value = entry.value;
    }
    std::cout << "column.size() = " << column.size() << std::endl;
    std::cout << "data_rows_count = " << data_rows_count << std::endl;
    assert(column.size() == data_rows_count);
    return column;
}

//void DecoderGAMPS::decodeColumnGroups(){
//    for(int i=0; i < mapping_table->baseColumnsCount(); i++){
//        int base_column_index = mapping_table->base_columns_indexes.at(i);
//        decodeColumnGroup(base_column_index);
//    }
//}

//void DecoderGAMPS::decodeColumnGroup(int base_column_index){
//    // decode base column
//    column_index = base_column_index;
//#if COUT
//    std::cout << "decode base column_index " << column_index << std::endl;
//#endif
//    dataset->setColumn(column_index);
//    std::vector<std::string> base_column = decodeBaseColumn();
//    dataset->updateRangesGAMPS(base_column_index);
//
//    // decode ratio columns
//    std::vector<int> column_group_indexes = mapping_table->ratioSignals(base_column_index);
//    for(int i=0; i < column_group_indexes.size(); i++){
//        column_index = column_group_indexes.at(i);
//    #if COUT
//        std::cout << "decode ratio column_index " << column_index << std::endl;
//    #endif
//        dataset->setColumn(column_index);
//        decodeRatioColumn(base_column);
//    }
//}

//std::vector<std::string> DecoderGAMPS::decodeBaseColumn(){
//#if MASK_MODE
//    mask = MaskDecoder::decode(this);
//#endif
//    std::vector<std::string> base_column = DecoderAPCA::decodeDataColumn(this);
//    columns.at(column_index) = base_column;
//    return base_column;
//}

//void DecoderGAMPS::decodeRatioColumn(std::vector<std::string> base_column){
//#if MASK_MODE
//    mask = MaskDecoder::decode(this);
//#endif
//    std::vector<std::string> diff_column = DecoderAPCA::decodeDataColumn(this);
//    std::vector<std::string> ratio_column;
//    for(int i=0; i < diff_column.size(); i++){
//        std::string ratio = calculateRatio(base_column.at(i), diff_column.at(i));
//        ratio_column.push_back(ratio);
//    }
//    columns.at(column_index) = ratio_column;
//}

//std::string DecoderGAMPS::calculateRatio(std::string base_value, std::string diff){
//    if (Constants::isNoData(base_value) || Constants::isNoData(diff)) { return diff; }
//
//    int ratio_value = StringUtils::stringToInt(diff) + StringUtils::stringToInt(base_value);
//    return StringUtils::intToString(ratio_value);
//}
