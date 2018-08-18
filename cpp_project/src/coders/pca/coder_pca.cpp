
#include "coder_pca.h"

#include "assert.h"

void CoderPCA::setCoderParams(int fixed_window_size_, std::vector<int> error_thresholds_vector_){
    fixed_window_size = fixed_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderPCA::codeColumnBefore(){
    window = createWindow();
}

void CoderPCA::codeColumnWhile(std::string csv_value){
    if (MASK_MODE && Constants::isNoData(csv_value)) { return; } // MASK_MODE => ignore no data

    window.addValue(csv_value);
    if (window.isFull()) { codeWindow(window); }
}

void CoderPCA::codeColumnAfter(){
    if (!window.isEmpty()) {
        assert(!window.isFull());
        codeNonConstantWindow(window);
    }
}

PCAWindow CoderPCA::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    return PCAWindow(fixed_window_size, error_threshold);
}

void CoderPCA::codeWindow(PCAWindow & window){
    if (window.hasConstantValue()){ codeConstantWindow(window); }
    else {                          codeNonConstantWindow(window);  }
    window.clearWindow();
}

void CoderPCA::codeConstantWindow(PCAWindow & window){
    codeBit(0);
    codeValueRaw(window.constant_value);
}

void CoderPCA::codeNonConstantWindow(PCAWindow & window){
    codeBit(1);
    for(int i=0; i < window.length; i++){
        std::string csv_value = window.getElement(i);
        codeValueRaw(csv_value);
    }
}
