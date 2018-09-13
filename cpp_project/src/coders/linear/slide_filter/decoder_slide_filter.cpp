
#include "decoder_slide_filter.h"

#include "math_utils.h"
#include <cmath>
#include "constants.h"

void DecoderSlideFilter::setCoderParams(int max_window_size_){
    max_window_size_bit_length = MathUtils::bitLength(max_window_size_);
}


std::vector<std::string> DecoderSlideFilter::decodeDataColumn(){
    std::vector<std::string> column;
    std::string previous_value = "random"; // any value that cannot be read from the csv
    row_index = 0;

    while (row_index < data_rows_count){
        decodeWindow(column);

        if (current_value == Constants::NO_DATA || previous_value == current_value || current_window_size == 1){
            for (int i=0; i < current_window_size; i++){
                column.push_back(current_value);
                row_index++;
            }
        }
        else {
            createWindow(column, previous_value);
        }
        previous_value = current_value;
    }
    return column;
}

void DecoderSlideFilter::decodeWindow(std::vector<std::string> & column){
    current_window_size = input_file.getInt(max_window_size_bit_length);
    current_value = decodeValueRaw();
}

void DecoderSlideFilter::createWindow(std::vector<std::string> & column, std::string previous_value){
//    int previous_value_int = StringUtils::stringToInt(previous_value);
//    int current_value_int = StringUtils::stringToInt(current_value);
//
//    CAPoint first_point = CAPoint(0, previous_value_int);
//    CAPoint last_point = CAPoint(current_window_size, current_value_int);
//    CALine line = CALine(first_point, last_point);
//
//    for (int i=0; i < current_window_size; i++){
//        CAPoint point = CAPoint(i + 1, 0); // y doesn't matter
//        double y = line.yIntersection(point);
//        int val = std::round(y);
//        std::string val_str = StringUtils::intToString(val);
//        column.push_back(val_str);
//        row_index++;
//        if (i == current_window_size - 1){
//            assert(val == current_value_int);
//        }
//    }
}
