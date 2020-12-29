
#include "coder_gamps.h"
#include "mask_coder.h"
#include "time_delta_coder.h"
#include "conversor.h"
#include "assert.h"
#include "vector_utils.h"
#include "coder_apca.h"
#include "gamps_utils.h"
#include "GAMPSInput.h"
#include "group_gamps.h"

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

    total_data_types = limit_mode ? dataset->dataColumnsGroupCount() : 1;
    total_data_type_columns = dataset->data_columns_count / total_data_types;
    gamps_epsilons_vector = getGAMPSEpsilonsVector();

//    std::cout << "VectorUtils::printIntVector(error_thresholds_vector);" << std::endl;
//    VectorUtils::printIntVector(error_thresholds_vector);
//    std::cout << "VectorUtils::printIntVector(gamps_epsilons_vector);" << std::endl;
//    VectorUtils::printIntVector(gamps_epsilons_vector);

    for(data_type_index = 1; data_type_index <= total_data_types; data_type_index++){
        codeDataTypeColumns();
    }
}

std::vector<int> CoderGAMPS::getGAMPSEpsilonsVector(){
    std::vector<int> epsilons_vector(total_data_types, -1);

//    std::cout << "total_data_types = " << total_data_types << std::endl;
    for(int i=1; i < error_thresholds_vector.size(); i++){ // skip the first entry (time delta epsilon)
        int data_type_index = (i - 1) % total_data_types; // -1 because the first entry is skipped
        int current_epsilon = epsilons_vector.at(data_type_index);
        int candidate_epsilon = error_thresholds_vector.at(i);
        if (current_epsilon == -1 or candidate_epsilon < current_epsilon){
            epsilons_vector.at(data_type_index) = candidate_epsilon;
        }
    }
    return epsilons_vector;
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

void CoderGAMPS::codeDataTypeColumns(){
    mapping_table = new MappingTable();
#if COUT
    std::cout << "ccode group " << data_type_index << "/" << total_data_types << std::endl;
#endif
    double epsilon = (double) gamps_epsilons_vector.at(data_type_index);
    GroupGAMPS* group_gamps = new GroupGAMPS(this, epsilon);
    GAMPSOutput* gamps_output = group_gamps->getGAMPSOutput(column_index);
    nodata_rows_mask = group_gamps->getMask();
    codeMappingTable(gamps_output);
    codeGAMPSColumns(gamps_output);
    delete group_gamps;
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

        column_index = MappingTable::mapIndex(table_index, total_data_types, data_type_index);
    #if COUT
        std::cout << "  code base  signal i = " << column_index << std::endl;
    #endif
        dataset->setColumn(column_index);
        column = base_signals[base_index++];
        codeGAMPSColumn(column, true); // CODE BASE COLUMN

        std::vector<int> ratio_columns = mapping_table->ratioColumns(table_index);
        for (int j = 0; j < ratio_columns.size(); j++){
            table_index = ratio_columns.at(j);
            column_index = MappingTable::mapIndex(table_index, total_data_types, data_type_index);
        #if COUT
            std::cout << "    code ratio signal i = " << column_index << std::endl;
        #endif
            dataset->setColumn(column_index);
            int ratio_index = mapping_table->getRatioGampsColumnIndex(table_index);
            column = ratio_signals[ratio_index];
            codeGAMPSColumn(column, false); // CODE RATIO COLUMN
        }
    }
}

void CoderGAMPS::codeGAMPSColumn(DynArray<GAMPSEntry>* column, bool base_window){
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

    APCAWindow* window = new APCAWindow(window_size, 0); // threshold will not be used TODO: why?
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
            codeWindow(window, base_window);
            window->addFirstValue(csv_value);
        }
        if (!no_data_row){
            update(column, entry_index, current_entry, remaining);
        }
    }
    if (!window->isEmpty()) {
        codeWindow(window, base_window);
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

void CoderGAMPS::codeWindow(APCAWindow* window, bool base_window){
    codeWindowLength((Window*) window);
    std::string constant_value = window->constant_value;
    if (base_window){
        // Code the window exactly the same way as it is done in the APCA coder
        // In order to call the codeValueRaw with the correct string, the mapValue mapping must be reverted
        if (!Constants::isNoData(constant_value)){
            constant_value = GroupGAMPS::unmapValue(constant_value, dataset->offset());
        }
        codeValueRaw(constant_value);
    }
    else {
        double value = Constants::NO_DATA_DOUBLE;
        if (!Constants::isNoData(constant_value)){
            value = Conversor::stringToDouble(constant_value);
        }
        codeFloat((float) value);
    }
}
