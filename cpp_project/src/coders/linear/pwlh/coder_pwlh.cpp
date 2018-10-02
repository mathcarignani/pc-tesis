
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
    delta_sum = 0;
    window = createWindow();
}

void CoderPWLH::codeColumnWhile(std::string csv_value){
    delta_sum += time_delta_vector[row_index];
#if MASK_MODE
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
#endif
    if (!window->conditionHolds(csv_value, delta_sum)){
        codeWindow(window);
        window->addFirstValue(csv_value);
    }
    delta_sum = 0;
}

void CoderPWLH::codeColumnAfter(){
    if (!window->isEmpty()){ codeWindow(window); }
}

PWLHWindow* CoderPWLH::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    Range column_range = dataset.column_code.range;
    return new PWLHWindow(max_window_size, error_threshold, column_range, integer_mode);
}

void CoderPWLH::codeWindow(PWLHWindow* window){
    codeInt(window->length, window->max_window_size_bit_length);
    (integer_mode) ? codeWindowInt(window) : codeWindowDouble(window);
}

void CoderPWLH::codeWindowDouble(PWLHWindow* window){
#if !MASK_MODE
    if (window->nan_window){
        codeFloat(FLT_MAX); // no need to code another value
        return;
    }
#endif
    if (window->length > 1) {
        float point1_y = window->getPoint1Y();
        float point2_y = window->getPoint2Y();
        codeFloat(point1_y);
        codeFloat(point2_y);
        return;
    }
    // window.length == 1 => this code can only run the last time codeWindow is called
    // IMPORTANT: window.constant_value_float is an int casted as a float
    codeFloat(window->constant_value_float); // no need to code another value
}

void CoderPWLH::codeWindowInt(PWLHWindow* window){
#if !MASK_MODE
    if (window->nan_window){
        codeValueRaw(window->constant_value); // no need to code another value
        return;
    }
#endif
    if (window->length > 1){
        std::string point1_y = window->getPoint1YIntegerMode();
        std::string point2_y = window->getPoint2YIntegerMode();
        codeValueRaw(point1_y);
        codeValueRaw(point2_y);
        return;
    }
    // window.length == 1 => this code can only run the last time codeWindow is called
    codeValueRaw(window->constant_value); // no need to code another value
}
