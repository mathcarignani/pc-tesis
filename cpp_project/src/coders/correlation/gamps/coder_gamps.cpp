
#include "coder_gamps.h"
#include "mask_coder.h"
#include "time_delta_coder.h"
#include "math_utils.h"
#include "assert.h"
#include "vector_utils.h"
#include "coder_apca.h"
#include "gamps_utils.h"
#include "coder_utils.h"
#include "GAMPS.h"
#include "GAMPSInput.h"

void CoderGAMPS::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    mapping_table = new MappingTable();
}

void CoderGAMPS::codeCoderParams(){
    codeCoderParameters(Constants::CODER_GAMPS, window_size);
}

void CoderGAMPS::codeDataRows(){
    codeTimeDeltaColumn();
    codeOtherColumns();
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

void CoderGAMPS::codeOtherColumns(){
    Mask* nodata_rows_mask = getNodataRowsMask();
    GAMPSInput* gamps_input = getGAMPSInput(nodata_rows_mask);
    GAMPSOutput* gamps_output = getGAMPSOutput(gamps_input);
    codeMappingTable(gamps_output);
    exit(1);
    codeColumnGroups(gamps_output);
}

GAMPSOutput* CoderGAMPS::getGAMPSOutput(GAMPSInput* gamps_input){
    double epsilon = 1000;
    GAMPS* gamps = new GAMPS(epsilon, gamps_input);
    gamps->compute();
    return gamps->getOutput();
}

Mask* CoderGAMPS::getNodataRowsMask(){
    Mask* mask = new Mask();
    std::vector<bool> nodata_columns(dataset->data_columns_count, true);

    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading) {
        std::vector<std::string> row = input_csv->readLineCSV();
        bool nodata_row = true;
        for(int i = 1; i < row.size(); i++){ // i = 1 to skip TimeDelta column
            std::string csv_value = row.at(i);
            if (!Constants::isNoData(csv_value)){
                nodata_row = false;
                nodata_columns[i-1] = false;
            }
        }
//        std::cout << (nodata_row ? "NODATA" : "DATA") << std::endl;
        mask->add(nodata_row);
    }
    mask->close();

    // add nodata columns indexes to the mapping_table
    for (int i = 0; i < dataset->data_columns_count; i++){
        int col_index = i + 1;
        if (nodata_columns[i]) { mapping_table->addNodataColumnIndex(col_index); }
    }
    return mask;
}

GAMPSInput* CoderGAMPS::getGAMPSInput(Mask* nodata_rows_mask){
    int data_columns_count = dataset->data_columns_count - mapping_table->nodata_columns_indexes.size();
    CMultiDataStream* multiStream = new CMultiDataStream(data_columns_count);
    for(int i = 0; i < dataset->data_columns_count; i++)
    {
        int col_index = i + 1;
        if (mapping_table->isNodataColumnIndex(col_index)) { continue; }

        std::cout << "Parsing column " << col_index << std::endl;

        dataset->setColumn(col_index);
        CDataStream* signal = getColumn(col_index, nodata_rows_mask);
        multiStream->addSingleStream(signal);
    }
    GAMPSInput* gamps_input = new GAMPSInput(multiStream);
    return gamps_input;
}

CDataStream* CoderGAMPS::getColumn(int column_index, Mask* nodata_rows_mask){
    CDataStream* dataStream = new CDataStream();

    nodata_rows_mask->reset();
    int timestamp = 0;
    int previous_value = -1;
    int value;

    std::cout << "getColumn " << column_index << std::endl;
    std::cout << "dataset->offset() = " << dataset->offset() << std::endl;

    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        std::string mapped_value = CoderUtils::mapValue(csv_value, dataset->offset() + 1);

        if (nodata_rows_mask->isNoData()){ continue; } // skip nodata rows

        timestamp++;

        if (Constants::isNoData(mapped_value)){
            if (previous_value == -1){ continue; }
            value = previous_value; // same as the last (no nodata) value
        }
        else {
            value = StringUtils::stringToInt(mapped_value);
            if (previous_value == -1 && timestamp > 0){ // the first rows of the column contained nodata values
                // fill previous values
                for(int i = 1; i < timestamp; i++){ dataStream->add(DataItem(value, i)); }
            }
            previous_value = value;
        }
        dataStream->add(DataItem(value, timestamp));
    }
    assert(timestamp > -1);
    assert(previous_value > -1);
    assert(timestamp == dataStream->size());
    assert(timestamp == data_rows_count - nodata_rows_mask->total_no_data);
    return dataStream;
}

void CoderGAMPS::codeMappingTable(GAMPSOutput* gamps_output){
    mapping_table->calculate(dataset->data_columns_count, gamps_output);
    mapping_table->print();
    exit(1);

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

    DynArray<GAMPSEntry>* column;
    DynArray<GAMPSEntry>** base_signals = gamps_output->getResultBaseSignal();
    DynArray<GAMPSEntry>** ratio_signals = gamps_output->getResultRatioSignal();

    for(int i = 0; i < dataset->data_columns_count; i++){
        if (gamps_output->getTgood()[i] == i){ // base signal
            std::cout << "code base signal i = " << i + 1 << std::endl;
            column = base_signals[base_count++];
        }
        else{ // ratio signal
            std::cout << "code ratio signal i = " << i + 1 << std::endl;
            column = ratio_signals[ratio_count++];
        }
        codeColumn(column);
    }
}

void CoderGAMPS::codeColumn(DynArray<GAMPSEntry>* column){
    std::cout << "array->size() = " << column->size() << std::endl;
    for(int i=0; i < column->size(); i++){
        GAMPSEntry entry = column->getAt(i);
        std::cout << "entry.value = " << entry.value << std::endl;
        std::cout << "entry.endingTimestamp = " << entry.endingTimestamp << std::endl;

        codeDouble(entry.value);
        codeInt(entry.endingTimestamp); // TODO: code size instead of timestamp
    }
}
