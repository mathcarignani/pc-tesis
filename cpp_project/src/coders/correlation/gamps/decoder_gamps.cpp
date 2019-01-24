
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
    std::vector<int> base_column_index_vector;
    for (int i = 0; i < dataset->data_columns_count; i++){
        int base_column_index = decodeInt(column_index_bit_length) + 1;
        base_column_index_vector.push_back(base_column_index);
    }
    mapping_table = new MappingTable(base_column_index_vector);
    mapping_table->print();
}

void DecoderGAMPS::decodeColumnGroups(){
    for(int i=0; i < mapping_table->baseColumnsCount(); i++){
        int base_column_index = mapping_table->base_columns_indexes.at(i);
        decodeColumnGroup(base_column_index);
    }
}

void DecoderGAMPS::decodeColumnGroup(int base_column_index){
    // decode base column
    column_index = base_column_index;
#if COUT
    std::cout << "decode base column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    std::vector<std::string> base_column = decodeBaseColumn();
    dataset->updateRangesGAMPS(base_column_index);

    // decode ratio columns
    std::vector<int> column_group_indexes = mapping_table->ratioSignals(base_column_index);
    for(int i=0; i < column_group_indexes.size(); i++){
        column_index = column_group_indexes.at(i);
    #if COUT
        std::cout << "decode ratio column_index " << column_index << std::endl;
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
