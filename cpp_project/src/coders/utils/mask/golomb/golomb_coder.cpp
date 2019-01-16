
#include "golomb_coder.h"
#include <math.h>
#include <iostream>
#include <stdlib.h>


GolombCoder::GolombCoder(CoderBase* coder_, double p_){
    coder = coder_;
    p = p_;
    l = calculateL(p_);
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
    coder->codeUnary(k);

    CSVReader* input_csv = coder->input_csv;
    input_csv->goToFirstDataRow(column_index);

    int no_data_count = 0;
    while (input_csv->continue_reading) {
        std::string csv_value = input_csv->readLineCSVWithIndex();
        if (Constants::isNoData(csv_value)){
            no_data_count++;
            continue;
        }
        codeRunLength(no_data_count);
        no_data_count = 0;
    }
    if (no_data_count > 0){ // the last entry is no-data
        codeRunLength(no_data_count);
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