
#include "coder_slide_filter.h"


void CoderSlideFilter::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderSlideFilter::codeColumn(){
    SlideFilterWindow window = createWindow();
    row_index = 0;
    input_csv.goToLine(4); // first data row
    while (input_csv.continue_reading){
        std::vector<std::string> csv_row = input_csv.readLineCSV();
        std::string csv_value = csv_row[column_index];
        if (!window.conditionHolds(csv_value)){
            codeWindow(window);
            window.addFirstValue(csv_value);
        }
        row_index++;
    }
    if (!window.isEmpty()){ codeWindow(window); }
}

SlideFilterWindow CoderSlideFilter::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    Range column_range = dataset.column_code.range;
    return SlideFilterWindow(max_window_size, error_threshold, column_range);
}

void CoderPWLH::codeWindow(PWLHWindow & window){
//    dataset.addBits(window.max_window_size_bit_length);
//    output_file.pushInt(window.length, window.max_window_size_bit_length);
//    if (window.nan_window){
//        codeValueRaw(window.constant_value); // no need to code another value
//    }
//    else if (window.length > 1){
//        std::string point1_y = window.getPoint1Y();
//        std::string point2_y = window.getPoint2Y();
//        codeValueRaw(point1_y);
//        codeValueRaw(point2_y);
//    }
//    else { // window.length == 1 => this code can only run the last time codeWindow is called
//        codeValueRaw(window.constant_value); // no need to code another value
//    }
}
