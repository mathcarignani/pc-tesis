
#include "decoder_gamps.h"
#include "string_utils.h"
#include "math_utils.h"
#include "time_delta_decoder.h"
#include "assert.h"
#include "gamps_utils.h"
#include "vector_utils.h"
#include "mask_decoder.h"
#include "decoder_apca.h"

void DecoderGAMPS::setCoderParams(int window_size_){
    window_size_bit_length = MathUtils::bitLength(window_size_);
}

void DecoderGAMPS::decodeDataRows(){
    int total_columns = dataset->data_columns_count + 1;
    columns = std::vector<std::vector<std::string>> (total_columns);

    decodeTimeDeltaColumn();
    decodeMapping();
    decodeColumnGroups();

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
    std::vector<int> decoded_column_indexes;
    for (int i = 0; i < dataset->data_columns_count; i++){
        int base_column_index = decodeInt(column_index_bit_length) + 1;
        decoded_column_indexes.push_back(base_column_index);
    }

    std::vector<MapEntry*> mapping_vector;
    std::vector<int> base_column_indexes;

    std::cout << "decoded_column_indexes" << std::endl;
    VectorUtils::printIntVector(decoded_column_indexes);

    for (int i = 0; i < decoded_column_indexes.size(); i++){
        int column_index = i + 1;
        int base_column_index = decoded_column_indexes.at(i);

        std::vector<int> ratio_signals;
        if (column_index == base_column_index){ // base column, must complete ratio_signals vector
            base_column_indexes.push_back(column_index);
            std::cout << "BASE" << std::endl;
            for (int j = 0; j < decoded_column_indexes.size(); j++){
                int column_index_j = j + 1;
                int base_column_index_j = decoded_column_indexes.at(j);
                std::cout << "base_column_index_j = " << base_column_index_j << std::endl;
                std::cout << "column_index = " << column_index << std::endl;
                std::cout << "base_column_index_j = " << base_column_index_j << std::endl;
                std::cout << "column_index_j = " << column_index_j << std::endl;

                if (base_column_index_j == column_index && base_column_index_j != column_index_j){
                    ratio_signals.push_back(column_index_j);
                }
            }
        }
        std::cout << "column_index = " << column_index << ", base_column_index = " << base_column_index << std::endl;
        VectorUtils::printIntVector(ratio_signals);
        MapEntry* map_entry = new MapEntry(column_index, base_column_index, ratio_signals);
        mapping_vector.push_back(map_entry);
    }
    mapping_table = new MappingTable(mapping_vector, base_column_indexes);
}

void DecoderGAMPS::decodeColumnGroups(){
    std::cout << "decodeColumnGroups()" << std::endl;
    std::cout << "mapping_table->baseColumnsCount() = " << mapping_table->baseColumnsCount() << std::endl;
    for(int i=0; i < mapping_table->baseColumnsCount(); i++){
        std::cout << "i = " << i << std::endl;
        int base_column_index = mapping_table->base_columns_indexes.at(i);
    #if COUT
        std::cout << "decode column group = " << base_column_index << std::endl;
    #endif
        decodeColumnGroup(base_column_index);
    }
}

void DecoderGAMPS::decodeColumnGroup(int base_column_index){
    // decode base column
    column_index = base_column_index;
#if COUT
    std::cout << "decode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    std::vector<std::string> base_column = decodeBaseColumn();
    dataset->updateRangesGAMPS(base_column_index);

    // decode ratio columns
    std::vector<int> column_group_indexes = mapping_table->ratioSignals(base_column_index);
    VectorUtils::printIntVector(column_group_indexes);
    for(int i=0; i < column_group_indexes.size(); i++){
        column_index = column_group_indexes.at(i);
    #if COUT
        std::cout << "decode column_index " << column_index << std::endl;
    #endif
        dataset->setColumn(column_index);
        decodeRatioColumn(base_column);
    }
}

std::vector<std::string> DecoderGAMPS::decodeBaseColumn(){
#if MASK_MODE
    mask = MaskDecoder::decode(this);
#endif
    std::vector<std::string> base_column = DecoderAPCA::decodeDataColumn(this);
    columns.at(column_index) = base_column;
    return base_column;
}

void DecoderGAMPS::decodeRatioColumn(std::vector<std::string> base_column){
#if MASK_MODE
    mask = MaskDecoder::decode(this);
#endif
    std::vector<std::string> diff_column = DecoderAPCA::decodeDataColumn(this);
    std::vector<std::string> ratio_column;
    for(int i=0; i < diff_column.size(); i++){
        std::string ratio = calculateRatio(base_column.at(i), diff_column.at(i));
        ratio_column.push_back(ratio);
    }
    columns.at(column_index) = ratio_column;
}

std::string DecoderGAMPS::calculateRatio(std::string base_value, std::string diff){
    if (Constants::isNoData(base_value) || Constants::isNoData(diff)) { return diff; }

    int ratio_value = StringUtils::stringToInt(diff) + StringUtils::stringToInt(base_value);
    return StringUtils::intToString(ratio_value);
}
