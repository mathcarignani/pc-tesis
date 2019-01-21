
#include "golomb_mask_coder.h"

#if MASK_MODE

#include "assert.h"
#include "golomb_coder.h"

int GolombMaskCoder::code(CoderBase* coder, int column_index){
    int total_data_rows = countTotalDataRows(coder, column_index);
    bool single_burst = total_data_rows == 0 || total_data_rows == coder->data_rows_count;
    coder->codeBool(single_burst);

    if (single_burst){ // p in {0, 1}
        bool no_data_burst = total_data_rows == 0;
        coder->codeBool(no_data_burst);
    }
    else { // 0 < p < 1
        GolombCoder* golomb_coder = new GolombCoder(coder, total_data_rows);
        golomb_coder->code(column_index);
    }
    return total_data_rows;
}

int GolombMaskCoder::countTotalDataRows(CoderBase* coder, int column_index){
    int total_data_rows = 0;
    CSVReader* input_csv = coder->input_csv;
    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading) {
        std::string csv_value = input_csv->readLineCSVWithIndex();
        if (!Constants::isNoData(csv_value)) { total_data_rows++; }
    }
    return total_data_rows;
}

#endif // MASK_MODE
