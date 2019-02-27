
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
    int column_index_bit_length = MathUtils::bitLength(vector_size);
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
    std::cout << "DecoderGAMPS::decodeGAMPSColumns()" << std::endl;
    for(int i = 0; i < mapping_table->gamps_columns_count; i++){
        column_index = mapping_table->getColumnIndex(i);
        if (!mapping_table->isBaseColumn(column_index)){ continue; }

        std::cout << "decode base  signal i = " << column_index << std::endl;
        dataset->setColumn(column_index);

        std::vector<int> ratio_columns = mapping_table->ratioColumns(column_index);
        int ratio_columns_size = ratio_columns.size();

        if (ratio_columns_size == 0){
            std::vector<std::string> base_column = decodeBaseColumn();
            columns.at(column_index) = base_column;
            continue;
        }

        std::vector<double> base_column_double;
        std::vector<std::string> base_column = decodeBaseColumn(base_column_double);
        columns.at(column_index) = base_column;

        for (int j = 0; j < ratio_columns.size(); j++){
            column_index = ratio_columns.at(j);
            std::cout << "    decode ratio signal i = " << column_index << std::endl;
            dataset->setColumn(column_index);
            std::vector<std::string> ratio_column = decodeRatioColumn(base_column_double);
            columns.at(column_index) = ratio_column;

            assert(ratio_column.size() == data_rows_count);
//            VectorUtils::printStringVector(ratio_column);
        }
    }
}

std::vector<std::string> DecoderGAMPS::decodeBaseColumn(){
    std::vector<double> read_column = decodeGAMPSColumn();
    assert(read_column.size() == data_rows_count);

    std::vector<std::string> base_column;
    for(int i = 0; i < read_column.size(); i++){
        double value = read_column.at(i);
        std::string csv_value = CoderUtils::unmapValueInt(value, dataset->offset() + 1);
        base_column.push_back(csv_value);
    }
    assert(base_column.size() == data_rows_count);
//    VectorUtils::printStringVector(base_column);
    std::cout << std::endl;
    return base_column;
}

std::vector<std::string> DecoderGAMPS::decodeBaseColumn(std::vector<double> & base_column_double){
    std::vector<double> read_column = decodeGAMPSColumn();
    assert(read_column.size() == data_rows_count);

    double previous_value = -1;
    std::vector<std::string> base_column;
    for(int i = 0; i < read_column.size(); i++){
        double value = read_column.at(i);
        std::string csv_value = CoderUtils::unmapValueInt(value, dataset->offset() + 1);
        base_column.push_back(csv_value);

        if (Constants::isNoData(value)){
            if (previous_value == -1) { continue; } // up to this point no integer has been read
            value = previous_value; // same as the previous integer value
        }
        else {
            if (previous_value == -1){ for(int j = 0; j < i; j++) { base_column_double.push_back(value); } }
            previous_value = value;
        }
        base_column_double.push_back(value);
    }
    assert(base_column_double.size() == data_rows_count);
    assert(base_column.size() == data_rows_count);
//    VectorUtils::printDoubleVector(base_column_double);
//    VectorUtils::printStringVector(base_column);
    std::cout << std::endl;
    return base_column;
}

std::vector<std::string> DecoderGAMPS::decodeRatioColumn(std::vector<double> base_column_double){
    std::vector<double> read_column = decodeGAMPSColumn();
    assert(read_column.size() == data_rows_count);

    std::vector<std::string> ratio_column;
    for(int i = 0; i < read_column.size(); i++){
        double value = read_column.at(i);
        std::string csv_value;

        if (Constants::isNoData(value)){
            ratio_column.push_back(Constants::NO_DATA);
            continue;
        }
        //
        // CODER:
        // - calculates value = ratio(i) / base(i)
        // - codes base(i) and value
        //
        // DECODER:
        // - decodes base(i) and value
        // - calculates ratio(i) = value * base(i)
        //
        double ratio_i = value * base_column_double.at(i);
//        std::cout << "ratio_i = value * base_column_double.at(i) = " << value << " * " << base_column_double.at(i) << " = " << ratio_i << std::endl;
        csv_value = CoderUtils::unmapValueInt(ratio_i, dataset->offset() + 1);
//        std::cout << "csv_value = " << csv_value << std::endl;
        ratio_column.push_back(csv_value);
    }
    assert(ratio_column.size() == data_rows_count);
//    VectorUtils::printStringVector(ratio_column);
    std::cout << std::endl;
    return ratio_column;
}

std::vector<double> DecoderGAMPS::decodeGAMPSColumn(){
    std::vector<double> column;
    row_index = 0;
    int unprocessed_rows = data_rows_count;

#if MASK_MODE
    mask = MaskDecoder::decode(this);
#if CHECKS
    assert(mask->total_no_data + mask->total_data == data_rows_count);
#endif // END CHECKS
#endif // END MASK_MODE

    while (unprocessed_rows > 0) {
    #if MASK_MODE
        if (mask->isNoData()) {
            column.push_back(Constants::NO_DATA_DOUBLE);
            row_index++; unprocessed_rows--;
            continue;
        }
    #endif
        decodeWindow(column);
        unprocessed_rows = data_rows_count - row_index;
    }
    return column;
}

void DecoderGAMPS::decodeWindow(std::vector<double> & column){
//    std::cout << "-----------------------------------------" << std::endl;
    int window_size = input_file->getInt(window_size_bit_length);
//    std::cout << "window_size = " << window_size << std::endl;
    decodeConstantWindow(column, window_size);
#if MASK_MODE
    mask->total_data -= window_size;
#endif
//    std::cout << "-----------------------------------------" << std::endl;
}

void DecoderGAMPS::decodeConstantWindow(std::vector<double> & column, int window_size){
    double constant = decodeDouble();
//    std::cout << "constant = " << constant << std::endl;
    int i = 0;
    while (i < window_size){
    #if MASK_MODE
        if (i > 0 && mask->isNoData()) { // always false in the first iteration
            column.push_back(Constants::NO_DATA_DOUBLE);
            row_index++;
            continue;
        }
    #endif
        column.push_back(constant);
        i++;
        row_index++;
    }
}
