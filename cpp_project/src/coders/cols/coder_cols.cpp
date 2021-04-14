
#include "coder_cols.h"

#include "assert.h"
#include "string_utils.h"
#include "arithmetic_mask_coder.h"
#include "time_delta_coder.h"
#include "coder_utils.h"

void CoderCols::codeDataRows(){
    int total_columns = dataset->data_columns_count + 1;
    column_index = 0;
    codeColumn();

#if MASK_MODE
    // mask all the columns (except the timestamps column)
    ArithmeticMaskCoder* amc = new ArithmeticMaskCoder(this, first_column_index, dataset->data_columns_count);
    total_data_rows_vector = amc->code();
#endif // !MASK_MODE

    for(column_index = 1; column_index < total_columns; column_index++) {
        codeColumn();
    }
}

void CoderCols::codeColumn() {
#if COUT
    std::cout << "ccode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    dataset->setMode("DATA");
#if MASK_MODE
    total_data_rows = total_data_rows_vector.at(column_index - first_column_index);
#endif // MASK_MODE
    codeDataColumn();
}

void CoderCols::codeDataColumn(){
    this->codeColumnBefore();

    row_index = 0;
    input_csv->goToFirstDataRow(column_index);
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        this->codeColumnWhile(csv_value);
        row_index++;
    }
    this->codeColumnAfter();
}
