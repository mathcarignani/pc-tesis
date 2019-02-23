
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
    TimeDeltaCoder::code(this);
}

GAMPSOutput* CoderGAMPS::processOtherColumns(){
    getNodataRowsMask();
    GAMPSInput* gamps_input = getGAMPSInput();
    GAMPSOutput* gamps_output = getGAMPSOutput(gamps_input);
    return gamps_output;
}

void CoderGAMPS::getNodataRowsMask(){
    nodata_rows_mask = new Mask();
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
        nodata_rows_mask->add(nodata_row);
    }
    nodata_rows_mask->close();
    mapping_table->setNoDataColumnsIndexes(nodata_columns, dataset->data_columns_count);
}

GAMPSInput* CoderGAMPS::getGAMPSInput(){
    int data_columns_count = dataset->data_columns_count - mapping_table->nodata_columns_indexes.size();
    CMultiDataStream* multiStream = new CMultiDataStream(data_columns_count);
    for(int i = 0; i < dataset->data_columns_count; i++)
    {
        int col_index = i + 1;
        if (mapping_table->isNodataColumnIndex(col_index)) { continue; } // skip nodata columns
        dataset->setColumn(col_index);
        CDataStream* signal = getColumn(col_index);
        multiStream->addSingleStream(signal);
    }
    GAMPSInput* gamps_input = new GAMPSInput(multiStream);
    return gamps_input;
}

CDataStream* CoderGAMPS::getColumn(int column_index){
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
//        std::cout << "codeInt(" << vector.at(i) << ", " << column_index_bit_length << ");" << std::endl;
        codeInt(vector.at(i), column_index_bit_length);
    }
}

void CoderGAMPS::codeGAMPSColumns(GAMPSOutput* gamps_output){
    DynArray<GAMPSEntry>** base_signals = gamps_output->getResultBaseSignal();
    DynArray<GAMPSEntry>** ratio_signals = gamps_output->getResultRatioSignal();

    DynArray<GAMPSEntry>* column;
    int base_index = 0;
    for(int i = 0; i < mapping_table->gamps_columns_count; i++){
        column_index = mapping_table->getColumnIndex(i);
        if (!mapping_table->isBaseColumn(column_index)){ continue; }

        std::cout << "code base  signal i = " << column_index << std::endl;
        std::cout << "base_index = " << base_index << std::endl;
        column = base_signals[base_index++];
        codeGAMPSColumn(column);

        std::vector<int> ratio_columns = mapping_table->ratioColumns(column_index);
        for (int j = 0; j < ratio_columns.size(); j++){
            column_index = ratio_columns.at(j);
            std::cout << "    code ratio signal i = " << column_index << std::endl;
            int ratio_index = mapping_table->getRatioGampsColumnIndex(column_index);
            std::cout << "    ratio_index = " << ratio_index << std::endl;
            column = ratio_signals[ratio_index];
            codeGAMPSColumn(column);
        }
    }
}

void CoderGAMPS::codeGAMPSColumn(DynArray<GAMPSEntry>* column){
#if MASK_MODE
    dataset->setMode("MASK");
    int total_data_rows = MaskCoder::code(this, column_index);
#endif
    dataset->setMode("DATA");

    int entry_index = 0;
    GAMPSEntry current_entry = column->getAt(entry_index);
    int remaining = current_entry.endingTimestamp;

    APCAWindow* window = new APCAWindow(window_size, 0); // threshold will not be used
    nodata_rows_mask->reset();
    row_index = 0;
    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading) {
        std::string csv_value = input_csv->readNextValue();

        bool no_data_row = nodata_rows_mask->isNoData();
        bool no_data = Constants::isNoData(csv_value);

    #if MASK_MODE
        // skip no_data
        if (no_data_row) { continue; }
        else if (no_data) {
            update(column, entry_index, current_entry, remaining);
            continue;
        }
    #endif
        csv_value = no_data ? csv_value : StringUtils::doubleToString(current_entry.value);

        if (!window->conditionHolds(csv_value)) {
            codeWindow(window);
            window->addFirstValue(csv_value);
        }
        if (!no_data_row){
            update(column, entry_index, current_entry, remaining);
        }

    }

    if (!window->isEmpty()) {
        codeWindow(window);
    }
}

void CoderGAMPS::update(DynArray<GAMPSEntry>* column, int & entry_index, GAMPSEntry & current_entry, int & remaining){
    remaining--;
    if (remaining > 0){ return; }

    entry_index++;
    if (entry_index == column->size()) { return; }

    int previous_last_timestamp = current_entry.endingTimestamp;
    current_entry = column->getAt(entry_index);
    remaining = current_entry.endingTimestamp - previous_last_timestamp;
}

void CoderGAMPS::codeWindow(APCAWindow* window){
    std::cout << "-----------------------------------------" << std::endl;
    codeInt(window->length, window->window_size_bit_length);
    std::cout << "codeInt(" << window->length << ", " << window->window_size_bit_length << ");" << std::endl;

    std::string constant_value = window->constant_value;
    double value = Constants::isNoData(constant_value) ? Constants::NO_DATA_DOUBLE : StringUtils::stringToDouble(constant_value);
    // TODO: move to an aux method... also create an analog decoding method
    codeDouble(value);
    std::cout << "codeDouble(" << value << ");" << std::endl;
    std::cout << "-----------------------------------------" << std::endl;
}
