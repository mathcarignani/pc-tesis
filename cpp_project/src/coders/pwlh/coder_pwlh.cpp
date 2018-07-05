
#include "coder_pwlh.h"

#include <cfloat>


void CoderPWLH::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_, bool integer_mode_){
    max_window_size = max_window_size_;
    integer_mode = integer_mode_;
    if (integer_mode) {
        // substract 1 to every error_threshold > 0
        for (int i=0; i < error_thresholds_vector_.size(); i++){
            int error_threshold = error_thresholds_vector_.at(i);
            if (error_threshold > 0) { error_threshold = error_threshold - 1; }
            error_thresholds_vector.push_back(error_threshold);
        }
    }
    else { // double mode
        error_thresholds_vector = error_thresholds_vector_;
    }
}

void CoderPWLH::codeColumnBefore(){
    window = createWindow();
}

void CoderPWLH::codeColumnWhile(std::string csv_value){
    if (!window.conditionHolds(csv_value)){
        codeWindow(window);
        window.addFirstValue(csv_value);
    }
}

void CoderPWLH::codeColumnAfter(){
    if (!window.isEmpty()){ codeWindow(window); }
}

PWLHWindow CoderPWLH::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    Range column_range = dataset.column_code.range;
    return PWLHWindow(max_window_size, error_threshold, column_range, integer_mode);
}

void CoderPWLH::codeWindow(PWLHWindow & window){
    dataset.addBits(window.max_window_size_bit_length);
    output_file.pushInt(window.length, window.max_window_size_bit_length);
    if (integer_mode) { codeWindowInt(window); } else { codeWindowDouble(window); }
}

void CoderPWLH::codeWindowDouble(PWLHWindow & window){
    if (window.nan_window){
//        std::cout << "D window.nan_window" << std::endl;
        codeFloat(FLT_MAX); // no need to code another value
    }
    else if (window.length > 1){
//        std::cout << "D window.length > 1" << std::endl;
        float point1_y = window.getPoint1Y();
        float point2_y = window.getPoint2Y();
        codeFloat(point1_y);
        codeFloat(point2_y);
    }
    else { // window.length == 1 => this code can only run the last time codeWindow is called
        // IMPORTANT: window.constant_value_float is an int casted as a float
//        std::cout << "D else" << std::endl;
        codeFloat(window.constant_value_float); // no need to code another value
    }
}

void CoderPWLH::codeWindowInt(PWLHWindow & window){
    if (window.nan_window){
//        std::cout << "I window.nan_window" << std::endl;
        codeValueRaw(window.constant_value); // no need to code another value
    }
    else if (window.length > 1){
//        std::cout << "I window.length > 1" << std::endl;
        std::string point1_y = window.getPoint1YIntegerMode();
        std::string point2_y = window.getPoint2YIntegerMode();
        codeValueRaw(point1_y);
        codeValueRaw(point2_y);
    }
    else { // window.length == 1 => this code can only run the last time codeWindow is called
//        std::cout << "I else" << std::endl;
        codeValueRaw(window.constant_value); // no need to code another value
    }
}
