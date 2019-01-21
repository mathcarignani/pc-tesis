
#include "simple_mask_coder.h"

#if MASK_MODE

#include "assert.h"

int SimpleMaskCoder::code(CoderBase* coder, int column_index){
    coder->dataset->setMaskMode(true);

    int total_data_rows = 0;
    Burst* burst = NULL;

    CSVReader* input_csv = coder->input_csv;
    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading) {
        std::string csv_value = input_csv->readLineCSVWithIndex();
        bool no_data = Constants::isNoData(csv_value);
        if (burst == NULL){ // first iteration
            burst = new Burst(no_data);
        }
        else if (no_data != burst->no_data || burst->length == Constants::MASK_MAX_SIZE){
            total_data_rows += codeBurst(coder, burst);
            burst = new Burst(no_data);
        }
        else {
            burst->increaseLength();
        }
    }
    assert(burst->length > 0);
    total_data_rows += codeBurst(coder, burst);
    return total_data_rows;
}

int SimpleMaskCoder::codeBurst(CoderBase* coder, Burst* burst){
    coder->codeBool(burst->no_data);
    coder->codeInt(burst->length - 1, Constants::MASK_BITS); // 1 <= burst->length <= Constants::MASK_MAX_SIZE
    return (burst->no_data ? 0 : burst->length);
}

#endif // MASK_MODE
