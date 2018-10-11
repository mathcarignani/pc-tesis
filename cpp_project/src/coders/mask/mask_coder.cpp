
#include "mask_coder.h"

#if MASK_MODE

#include "assert.h"

int MaskCoder::code(CoderBase* coder, Dataset* dataset, CSVReader* input_csv, int column_index){
    dataset->setMaskMode(true);

    bool burst_is_no_data = false;
    int burst_length = 0; // <= Constants::MASK_MAX_SIZE
    int total_data_rows = 0;
    bool first_entry = true;

    input_csv->goToFirstDataRow();
    while (input_csv->continue_reading) {
        std::string csv_value = input_csv->readLineCSVWithIndex(column_index);
        bool no_data = Constants::isNoData(csv_value);
        if (first_entry){
            first_entry = false;
            burst_is_no_data = no_data;
            burst_length = 1;
        }
        else if (no_data != burst_is_no_data || burst_length == Constants::MASK_MAX_SIZE){
            total_data_rows += codeBurst(coder, burst_is_no_data, burst_length);
            burst_is_no_data = no_data;
            burst_length = 1;
        }
        else {
            burst_length++;
        }
    }
    assert(burst_length > 0);
    total_data_rows += codeBurst(coder, burst_is_no_data, burst_length);
    return total_data_rows;
}

int MaskCoder::codeBurst(CoderBase* coder, bool burst_is_no_data, int burst_length){
    coder->codeBool(burst_is_no_data);
    coder->codeInt(burst_length - 1, Constants::MASK_BITS); // 1<= burst_length <= Constants::MASK_MAX_SIZE
    return (burst_is_no_data ? 0 : burst_length);
}

#endif
