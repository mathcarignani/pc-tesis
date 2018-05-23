
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
        std::vector<std::string> csv_row = input_csv.readLineCSV();
        std::string csv_value = csv_row[column_index];

//        std::cout << row_index << std::endl;
//        std::cout << "csv_value " << csv_value << std::endl;
        window.addValue(csv_value);
//        std::cout << "after window.addValue(csv_value);" << std::endl;
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
//    std::cout << "CodeWindow BEGIN" << std::endl;
    if (window.hasConstantValue()){
        codeWindowAsConstant(window);
    }
    else {
        codeWindowEachValue(window);
    }
    window.clearWindow();
//    std::cout << "CodeWindow END" << std::endl;
}

void CoderPCA::codeWindowAsConstant(PCAWindow & window){
    codeBit(0);
    codeValueRaw(window.constant_value);
//    std::cout << "constant " << window.constant_value << std::endl;
}

void CoderPCA::codeWindowEachValue(PCAWindow & window){
    codeBit(1);
    for(int i=0; i < window.length; i++){
        std::string csv_value = window.getElement(i);
        codeValueRaw(csv_value);
//        std::cout << "window " << csv_value << std::endl;
    }
}

std::string CoderPCA::getInfo() {
    return "a";
}
