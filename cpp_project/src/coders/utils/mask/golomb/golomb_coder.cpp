
#include "golomb_coder.h"
#include <math.h>
#include <iostream>
#include <stdlib.h>
#include <assert.h>


GolombCoder::GolombCoder(CoderBase* coder_, int total_data_rows){
    coder = coder_;
    int total_no_data_rows = coder->data_rows_count - total_data_rows;
    no_data_majority = total_no_data_rows > total_data_rows;
    if (no_data_majority){
        p = (double) total_no_data_rows / coder->data_rows_count;
    }
    else {
        p = (double) total_data_rows / coder->data_rows_count;
    }
#if CHECKS
    assert(p > 0.5);
#endif
    l = calculateL(p);
    k = nearestK(l);
}

int GolombCoder::calculateL(double p){
    int l=1;
    double inf=pow(p,l) + pow(p,l+1);
    double sup=pow(p,l) + pow(p,l-1);

    while ((inf>1) || (1>=sup)){
        l++;
        inf=pow(p,l) + pow(p,l+1);
        sup=pow(p,l) + pow(p,l-1);
    }
    return l;
}

int GolombCoder::nearestK(int & l){
    int k = 0;
    int current_value = 1;

    while (current_value < l){
        k++;
        current_value = (int) pow(2, k);
    }
    l = current_value;
    return k;
}

void GolombCoder::code(int column_index){
    coder->codeBool(no_data_majority);
    coder->codeUnary(k);

    CSVReader* input_csv = coder->input_csv;
    input_csv->goToFirstDataRow(column_index);

    int count = 0;
    while (input_csv->continue_reading) {
        std::string csv_value = input_csv->readNextValue();
        if (no_data_majority == Constants::isNoData(csv_value)){
            count++;
            continue;
        }
        codeRunLength(count);
        count = 0;
    }
    if (count > 0){
        codeRunLength(count);
    }
}

void GolombCoder::codeRunLength(int length){
    if (k == 0){
        coder->codeUnary(length);
        return;
    }
    // k > 0, l > 1
    div_t result = div(length, l); // length = l*result.quot + result.rem
    coder->codeUnary(result.quot);
    coder->codeInt(result.rem, k);
}
