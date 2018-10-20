
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

void DecoderGAMPS::decodeColumnGroups(){
    for(int i=0; i < dataset->dataColumnsGroupCount(); i++){
    #if COUT
        std::cout << "decode column group = " << i << std::endl;
    #endif
        decodeColumnGroup(i);
    }
}

void DecoderGAMPS::decodeColumnGroup(int group_index){
    std::vector<int> column_group_indexes = GAMPSUtils::columnGroupIndexes(dataset, group_index);
    VectorUtils::printIntVector(column_group_indexes);

    // decode base column
    column_index = column_group_indexes.at(0);
#if COUT
    std::cout << "decode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    std::vector<std::string> base_column = decodeBaseColumn();
    dataset->updateRangesGAMPS();

    // decode ratio columns
    for(int i=1; i < column_group_indexes.size(); i++){
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
