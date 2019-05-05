
#include "coder_gamps.h"
#include "mask_coder.h"
#include "time_delta_coder.h"
#include "conversor.h"
#include "assert.h"
#include "vector_utils.h"
#include "coder_apca.h"
#include "gamps_utils.h"
#include "coder_utils.h"
#include "GAMPSInput.h"

void CoderGAMPS::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_, bool limit_mode_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    limit_mode = limit_mode_;
}

void CoderGAMPS::codeCoderParams(){
    int coder_code = limit_mode ? Constants::CODER_GAMPS_LIMIT : Constants::CODER_GAMPS;
    codeCoderParameters(coder_code, window_size);
}

void CoderGAMPS::codeDataRows(){
    codeTimeDeltaColumn();

#if MASK_MODE == 3
    ArithmeticMaskCoder* amc = new ArithmeticMaskCoder(this, dataset->data_columns_count);
    total_data_rows_vector = amc->code();
#endif // MASK_MODE == 3

    total_groups = limit_mode ? dataset->dataColumnsGroupCount() : 1;
    total_group_columns = dataset->data_columns_count / total_groups;
    for(group_index = 1; group_index <= total_groups; group_index++){
        codeGroup();
    }
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

void CoderGAMPS::codeGroup(){
    mapping_table = new MappingTable();
#if COUT
    std::cout << "ccode group " << group_index << "/" << total_groups << std::endl;
#endif
    GAMPSOutput* gamps_output = processOtherColumns();
    codeMappingTable(gamps_output);
    codeGAMPSColumns(gamps_output);
    // free memory as in benchmarkLinux
    delete gamps_input;
    // delete gamps;
}

GAMPSOutput* CoderGAMPS::processOtherColumns(){
    getNodataRowsMask();
    gamps_input = getGAMPSInput();
    GAMPSOutput* gamps_output = getGAMPSOutput();
    return gamps_output;
}

void CoderGAMPS::getNodataRowsMask(){
    nodata_rows_mask = new Mask();
    std::vector<bool> nodata_columns(total_group_columns, true);

    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading) {
        std::vector<std::string> row = input_csv->readLineCSV();
        bool nodata_row = true;
        int j = 0;
        for(int i = group_index; i < row.size(); i+=total_groups){ // i > 0 to skip TimeDelta column
            std::string csv_value = row.at(i);
            if (!Constants::isNoData(csv_value)){
                nodata_row = false;
                nodata_columns[j] = false;
            }
            j++;
        }
        nodata_rows_mask->add(nodata_row);
    }
    nodata_rows_mask->close();
    mapping_table->setNoDataColumnsIndexes(nodata_columns, total_group_columns);
}

GAMPSInput* CoderGAMPS::getGAMPSInput(){
    gamps_epsilons_vector.clear();
    int data_columns_count = total_group_columns - mapping_table->nodata_columns_indexes.size();
    CMultiDataStream* multiStream = new CMultiDataStream(data_columns_count);
    int j = 1;
    for(int i = group_index; i <= dataset->data_columns_count; i+=total_groups){
        if (mapping_table->isNodataColumnIndex(j++)) { continue; } // skip nodata columns
        gamps_epsilons_vector.push_back(error_thresholds_vector.at(i));
        dataset->setColumn(i);
        CDataStream* signal = getColumn(i);
        multiStream->addSingleStream(signal);
    }
    return new GAMPSInput(multiStream);
}

CDataStream* CoderGAMPS::getColumn(int column_index){
//    std::cout << "BEGIN getColumn" << std::endl;
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
        // std::cout << "add(DataItem(" << current_value << ", " << timestamp << ")" << std::endl;
        dataStream->add(DataItem(current_value, timestamp));
    }
    assert(timestamp > 0);
    assert(previous_value > -1);
    assert(timestamp == dataStream->size());
    assert(timestamp == data_rows_count - nodata_rows_mask->total_no_data);
    return dataStream;
}

GAMPSOutput* CoderGAMPS::getGAMPSOutput(){
#if CHECKS
    assert(gamps_epsilons_vector.size() == gamps_input->getNumOfStream());
#endif
    gamps = new GAMPS(gamps_epsilons_vector, gamps_input);
    gamps->compute();
    return gamps->getOutput();
}

void CoderGAMPS::codeMappingTable(GAMPSOutput* gamps_output){
    mapping_table->calculate(gamps_output);
    // mapping_table->print(total_groups, group_index);

    std::vector<int> vector = mapping_table->baseColumnIndexVector();
    int vector_size = vector.size();
#if CHECKS
    assert(vector_size == total_group_columns);
#endif
    int column_index_bit_length = MathUtils::bitLength(vector_size);
    for (int i = 0; i < vector_size; i++){
        codeInt(vector.at(i), column_index_bit_length);
    }
}

void CoderGAMPS::codeGAMPSColumns(GAMPSOutput* gamps_output){
    DynArray<GAMPSEntry>** base_signals = gamps_output->getResultBaseSignal();
    DynArray<GAMPSEntry>** ratio_signals = gamps_output->getResultRatioSignal();

    DynArray<GAMPSEntry>* column;
    int base_index = 0;
    for(int i = 0; i < mapping_table->gamps_columns_count; i++){
        int table_index = mapping_table->getColumnIndex(i);
        if (!mapping_table->isBaseColumn(table_index)){ continue; }

        column_index = MappingTable::mapIndex(table_index, total_groups, group_index);
    #if COUT
        std::cout << "code base  signal i = " << column_index << std::endl;
    #endif
        dataset->setColumn(column_index);
        column = base_signals[base_index++];
        codeGAMPSColumn(column);

        std::vector<int> ratio_columns = mapping_table->ratioColumns(table_index);
        for (int j = 0; j < ratio_columns.size(); j++){
            table_index = ratio_columns.at(j);
            column_index = MappingTable::mapIndex(table_index, total_groups, group_index);
        #if COUT
            std::cout << "    code ratio signal i = " << column_index << std::endl;
        #endif
            dataset->setColumn(column_index);
            int ratio_index = mapping_table->getRatioGampsColumnIndex(table_index);
            column = ratio_signals[ratio_index];
            codeGAMPSColumn(column);
        }
    }
}

void CoderGAMPS::codeGAMPSColumn(DynArray<GAMPSEntry>* column){
#if MASK_MODE
#if MASK_MODE == 3
    total_data_rows_vector.at(column_index - 1);
#else
    dataset->setMode("MASK");
    MaskCoder::code(this, column_index);
#endif // MASK_MODE == 3
#endif // MASK_MODE

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
        csv_value = no_data ? csv_value : Conversor::doubleToString(current_entry.value);

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
    codeWindowLength((Window*) window);
    std::string constant_value = window->constant_value;
    double value = Constants::isNoData(constant_value) ? Constants::NO_DATA_DOUBLE : Conversor::stringToDouble(constant_value);
    // TODO: move to an aux method... also create an analog decoding method
    codeDouble(value);
}
