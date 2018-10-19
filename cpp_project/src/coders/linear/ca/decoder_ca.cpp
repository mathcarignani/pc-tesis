
#include "decoder_ca.h"
#include "string_utils.h"
#include "math_utils.h"
#include "ca_line.h"
#include <cmath>

void DecoderCA::setCoderParams(int window_size_){
    window_size_bit_length = MathUtils::bitLength(window_size_);
}


std::vector<std::string> DecoderCA::decodeDataColumn(){
    std::vector<std::string> column;
    std::string archived_value = "random"; // any value that cannot be read from the csv
    row_index = 0;

    while (row_index < data_rows_count){
        decodeWindow(column);

        if (current_window_size == 1){
            column.push_back(current_value);
            row_index++;
        }
        else if (current_value == Constants::NO_DATA){
            for (int i=0; i < current_window_size; i++){
                column.push_back(current_value);
                row_index++;
            }
        }
        else {
            createWindow(column, archived_value);
        }
        archived_value = current_value;
    }
    return column;
}

void DecoderCA::decodeWindow(std::vector<std::string> & column){
    current_window_size = input_file->getInt(window_size_bit_length);
    current_value = decodeValueRaw();
}

void DecoderCA::createWindow(std::vector<std::string> & column, std::string archived_value){
    int archived_value_int = StringUtils::stringToInt(archived_value);
    int current_value_int = StringUtils::stringToInt(current_value);

    CAPoint first_point = CAPoint(0, archived_value_int);
    int last_point_time_delta = 0;
    for (int i=0; i < current_window_size; i++){ last_point_time_delta += time_delta_vector.at(row_index + i); }
    CAPoint last_point = CAPoint(last_point_time_delta, current_value_int);
    CALine line = CALine(first_point, last_point);

    int current_sum = 0;
    int time_delta = 0;

    for (int i=0; i < current_window_size; i++){
        time_delta = time_delta_vector.at(row_index);
        if (i > 0) { assert(time_delta > 0); }
        current_sum += time_delta;

        CAPoint point = CAPoint(current_sum, 0); // y doesn't matter
        double y = line.yIntersection(point);
        int val = std::round(y);
        std::string val_str = StringUtils::intToString(val);
        column.push_back(val_str);
        row_index++;
        if (i == current_window_size - 1){
            assert(val == current_value_int);
        }
    }
}
