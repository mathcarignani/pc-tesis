
#include "coder_pwlh.h"

#include <cfloat>


void CoderPWLH::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_){
    integer_mode = coder_name == "CoderPWLHInt";
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderPWLH::codeColumnBefore(){
    delta_sum = 0;
    window = createWindow();
}

void CoderPWLH::codeColumnWhile(std::string csv_value){
    delta_sum += time_delta_vector[row_index]; // >= 0
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
    float error_threshold = error_thresholds_vector.at(column_index);
    if (integer_mode && error_threshold > 0){ error_threshold -= 0.5; }
    Range* column_range = dataset->column_code->range;
    return new PWLHWindow(window_size, error_threshold, column_range, integer_mode);
}

void CoderPWLH::codeWindow(PWLHWindow* window){
    codeWindowLength((Window*) window);
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
