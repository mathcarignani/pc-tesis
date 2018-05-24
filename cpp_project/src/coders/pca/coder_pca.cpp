
#include "coder_pca.h"

#include "assert.h"

void CoderPCA::setCoderParams(int fixed_window_size_, std::vector<int> error_thresholds_vector_){
    fixed_window_size = fixed_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderPCA::codeColumn(){
    PCAWindow window = createWindow();
    row_index = 0;
    input_csv.goToLine(4); // first data row
    while (input_csv.continue_reading){
        std::string csv_value = input_csv.readLineCSVWithIndex(column_index);
        window.addValue(csv_value);
        if (window.isFull()) { codeWindow(window); }
        row_index++;
    }
    if (!window.isEmpty()) {
        assert(!window.isFull());
        codeWindowEachValue(window);
    }
}

PCAWindow CoderPCA::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    return PCAWindow(fixed_window_size, error_threshold);
}

void CoderPCA::codeWindow(PCAWindow & window){
    if (window.hasConstantValue()){ codeWindowAsConstant(window); }
    else {                          codeWindowEachValue(window);  }
    window.clearWindow();
}

void CoderPCA::codeWindowAsConstant(PCAWindow & window){
    codeBit(0);
    codeValueRaw(window.constant_value);
}

void CoderPCA::codeWindowEachValue(PCAWindow & window){
    codeBit(1);
    for(int i=0; i < window.length; i++){
        std::string csv_value = window.getElement(i);
        codeValueRaw(csv_value);
    }
}

std::string CoderPCA::getInfo() {
    return "a";
}
