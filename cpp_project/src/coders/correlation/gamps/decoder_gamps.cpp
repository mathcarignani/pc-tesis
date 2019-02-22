
#include <coders/utils/coder_utils.h>
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
    decodeMappingTable();
    decodeNoDataColumns();
    decodeGAMPSColumns();

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

void DecoderGAMPS::decodeMappingTable(){
    int vector_size = dataset->data_columns_count;
    int column_index_bit_length = MathUtils::bitLength(vector_size - 1);
    std::vector<int> vector;
    for (int i = 0; i < vector_size; i++){
        int base_column_index = decodeInt(column_index_bit_length);
        std::cout << "base_column_index = " << base_column_index << std::endl;
        vector.push_back(base_column_index);
    }
    mapping_table = new MappingTable(vector);
    mapping_table->print();
}

void DecoderGAMPS::decodeNoDataColumns(){
    for(int i = 0; i < mapping_table->nodata_columns_indexes.size(); i++){
        int nodata_column_index = mapping_table->nodata_columns_indexes.at(i);
        std::vector<std::string> column(data_rows_count, Constants::NO_DATA);
        columns.at(nodata_column_index) = column;
    }
}

void DecoderGAMPS::decodeGAMPSColumns(){
    std::cout << "std::vector<std::vector<double>> base_columns = decodeGAMPSGroup(true);" << std::endl;
    std::vector<std::vector<double>> base_columns = decodeGAMPSGroup(true);
    std::cout << "std::vector<std::vector<double>> ratio_columns = decodeGAMPSGroup(false);" << std::endl;
    std::vector<std::vector<double>> ratio_columns = decodeGAMPSGroup(false);

    for(int i=0; i < base_columns.size(); i++){
        std::vector<double> base_column = base_columns.at(i);
        std::vector<std::string> column;
        column_index = mapping_table->base_columns_indexes.at(i);
        std::cout << "decode base  signal i = " << column_index << std::endl;
        assert(base_column.size() == data_rows_count);
        for(int j = 0; j < base_column.size(); j++){
            double value = base_column.at(j);
            std::string constant = CoderUtils::unmapValueInt(value, dataset->offset() + 1);
            column.push_back(constant);
        }
        assert(column.size() == data_rows_count);
        VectorUtils::printDoubleVector(base_column);
        VectorUtils::printStringVector(column);
        columns.at(column_index) = column;
    }

    for(int i=0; i < ratio_columns.size(); i++){
        std::vector<double> ratio_column = ratio_columns.at(i);
        std::vector<std::string> column;
        column_index = mapping_table->ratioColumnsIndexesAt(i);
        std::cout << "decode ratio signal i = " << column_index << std::endl;
        assert(ratio_column.size() == data_rows_count);
        for(int j = 0; j < ratio_column.size(); j++){
            double value = ratio_column.at(j);
            std::string constant = CoderUtils::unmapValueInt(value, dataset->offset() + 1);
            column.push_back(constant);
        }
        assert(column.size() == data_rows_count);
        VectorUtils::printDoubleVector(ratio_column);
        VectorUtils::printStringVector(column);
        columns.at(column_index) = column;
    }
}

std::vector<std::vector<double>> DecoderGAMPS::decodeGAMPSGroup(bool base_signals){
    std::vector<std::vector<double>> columns;
    std::vector<std::string> col;
    for(int i = 0; i < mapping_table->gamps_columns_count; i++){
        column_index = mapping_table->getColumnIndex(i);
        dataset->setColumn(column_index);
        bool base_column = mapping_table->isBaseColumn(column_index);
        if (base_signals != base_column){ continue; }
        std::cout << "decode " << (base_column ? "base " : "ratio") << " signal i = " << column_index << std::endl;
        std::vector<double> column = decodeGAMPSColumn(base_column);
        columns.push_back(column);
    }
    return columns;
}

std::vector<double> DecoderGAMPS::decodeGAMPSColumn(bool base_column){
    std::vector<double> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;

#if MASK_MODE
    Mask* mask = decoder->mask;
#if CHECKS
    assert(mask->total_no_data + mask->total_data == decoder->data_rows_count);
#endif // END CHECKS
#endif // END MASK_MODE

    while (unprocessed_rows > 0) {
    #if MASK_MODE
        if (mask->isNoData()) {
            column.push_back(Constants::NO_DATA_DOUBLE);
            decoder->row_index++; unprocessed_rows--;
            continue;
        }
    #endif
        decodeWindow(column, base_column);
        unprocessed_rows = data_rows_count - row_index;
    }
    return column;
}

void DecoderGAMPS::decodeWindow(std::vector<double> & column, bool base_column){
    std::cout << "-----------------------------------------" << std::endl;
    int window_size = input_file->getInt(window_size_bit_length);
    std::cout << "window_size = " << window_size << std::endl;
    decodeConstantWindow(column, window_size, base_column);
#if MASK_MODE
    decoder->mask->total_data -= window_size;
#endif
    std::cout << "-----------------------------------------" << std::endl;
}

void DecoderGAMPS::decodeConstantWindow(std::vector<double> & column, int window_size, bool base_column){
    // TODO: can use an integer for the base columns!
    double constant = base_column ? decodeInt() : decodeDouble();
    std::cout << "constant = " << constant << std::endl;
    int i = 0;
    while (i < window_size){
    #if MASK_MODE
        if (i > 0 && decoder->mask->isNoData()) { // always false in the first iteration
            column.push_back(Constants::NO_DATA_DOUBLE);
            decoder->row_index++;
            continue;
        }
    #endif
        column.push_back(constant);
        i++;
        row_index++;
    }
}
