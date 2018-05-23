
#include "coder_pca.h"

void CoderPCA::codeColumn(){
    PCAWindow window = PCAWindow(10, 5); // dataset.error_threshold, dataset.window_param);
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
    if (!window.isEmpty()) { codeWindow(window); }
}

void CoderPCA::codeWindow(PCAWindow & window){
//    std::cout << "CodeWindow BEGIN" << std::endl;
    if (window.hasConstantValue()){
        codeBit(0);
        codeValueRaw(window.constant_value);
    }
    else {
        codeBit(1);
        for(int i=0; i < window.length; i++){
            std::string csv_value = window.getElement(i);
            codeValueRaw(csv_value);
        }
    }
    window.clearWindow();
//    std::cout << "CodeWindow END" << std::endl;
}

std::string CoderPCA::getInfo() {
    return "a";
}
