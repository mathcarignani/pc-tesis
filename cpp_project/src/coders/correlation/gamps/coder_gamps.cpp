
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
    GAMPSOutput* gamps_output = processOtherColumns();
    codeMappingTable(gamps_output);
    codeGAMPSColumns(gamps_output);
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

GAMPSOutput* CoderGAMPS::processOtherColumns(){
    Mask* nodata_rows_mask = getNodataRowsMask();
    GAMPSInput* gamps_input = getGAMPSInput(nodata_rows_mask);
    GAMPSOutput* gamps_output = getGAMPSOutput(gamps_input);
    return gamps_output;
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
        mask->add(nodata_row);
    }
    mask->close();
    mapping_table->setNoDataColumnsIndexes(nodata_columns, dataset->data_columns_count);
    return mask;
}

GAMPSInput* CoderGAMPS::getGAMPSInput(Mask* nodata_rows_mask){
    int data_columns_count = dataset->data_columns_count - mapping_table->nodata_columns_indexes.size();
    CMultiDataStream* multiStream = new CMultiDataStream(data_columns_count);
    for(int i = 0; i < dataset->data_columns_count; i++)
    {
        int col_index = i + 1;
        if (mapping_table->isNodataColumnIndex(col_index)) { continue; } // skip nodata columns
        dataset->setColumn(col_index);
        CDataStream* signal = getColumn(col_index, nodata_rows_mask);
        multiStream->addSingleStream(signal);
    }
    GAMPSInput* gamps_input = new GAMPSInput(multiStream);
    return gamps_input;
}

CDataStream* CoderGAMPS::getColumn(int column_index, Mask* nodata_rows_mask){
    std::cout << "BEGIN getColumn" << std::endl;
    CDataStream* dataStream = new CDataStream();

    nodata_rows_mask->reset();
    int first_timestamp = 1;  // the first timestamp is always 1
    int timestamp = first_timestamp - 1;
    int previous_value = -1;
    int current_value;

    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        if (nodata_rows_mask->isNoData()){ continue; } // skip nodata rows

        timestamp++;

        if (Constants::isNoData(csv_value)){
            if (previous_value == -1){ continue; } // up to this point no integer has been read
            current_value = previous_value; // same as the previous integer value
        }
        else {
            current_value = CoderUtils::mapValueInt(csv_value, dataset->offset() + 1);
            if (previous_value == -1 && timestamp > first_timestamp){
                // the first rows of the column were nodata so we must fill them with current_value
                for(int i = first_timestamp; i < timestamp; i++){ dataStream->add(DataItem(current_value, i)); }
            }
            previous_value = current_value;
        }
        std::cout << "add(DataItem(" << current_value << ", " << timestamp << ")" << std::endl;
        dataStream->add(DataItem(current_value, timestamp));
    }
    assert(timestamp > 0);
    assert(previous_value > -1);
    assert(timestamp == dataStream->size());
    assert(timestamp == data_rows_count - nodata_rows_mask->total_no_data);
    return dataStream;
}

GAMPSOutput* CoderGAMPS::getGAMPSOutput(GAMPSInput* gamps_input){
    double epsilon = 0;
    // TODO: instead of a single epsilon, pass a list of epsilons (one for each stream)
    GAMPS* gamps = new GAMPS(epsilon, gamps_input);
    gamps->compute();
    return gamps->getOutput();
}

void CoderGAMPS::codeMappingTable(GAMPSOutput* gamps_output){
    mapping_table->calculate(gamps_output);
    mapping_table->print();

    std::vector<int> vector = mapping_table->baseColumnIndexVector();
    int vector_size = vector.size();
#if CHECKS
    assert(vector_size == dataset->data_columns_count);
#endif
    int column_index_bit_length = MathUtils::bitLength(vector_size - 1);
    for (int i = 0; i < vector_size; i++){
        std::cout << "codeInt(" << vector.at(i) << ", " << column_index_bit_length << ");" << std::endl;
        codeInt(vector.at(i), column_index_bit_length);
    }
}

void CoderGAMPS::codeGAMPSColumns(GAMPSOutput* gamps_output){
    int base_count = 0;
    int ratio_count = 0;

    DynArray<GAMPSEntry>* column;
    DynArray<GAMPSEntry>** base_signals = gamps_output->getResultBaseSignal();
    DynArray<GAMPSEntry>** ratio_signals = gamps_output->getResultRatioSignal();

    for(int i = 0; i < mapping_table->gamps_columns_count; i++){
        int col_index = mapping_table->getColumnIndex(i);
        if (mapping_table->isBaseColumn(col_index)){ // base column
            std::cout << "code base  signal i = " << col_index << std::endl;
            column = base_signals[base_count++];
        }
        else{ // ratio column
            std::cout << "code ratio signal i = " << col_index << std::endl;
            column = ratio_signals[ratio_count++];
        }
//        codeColumn(column);
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
