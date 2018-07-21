
#include "decoder_ca.h"

#include "string_utils.h"
#include "ca_line.h"
#include <cmath>

void DecoderCA::setCoderParams(int max_window_size_){
    max_window_size_bit_length = StringUtils::bitLength(max_window_size_);
}


std::vector<std::string> DecoderCA::decodeColumn(){
    std::vector<std::string> column;
    std::string previous_value = "random"; // any value that cannot be read from the csv
    row_index = 0;

    while (row_index < data_rows_count){
        std::cout << "row_index = " << row_index << std::endl;
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

void DecoderCA::decodeWindow(std::vector<std::string> & column){
    current_window_size = input_file.getInt(max_window_size_bit_length);
    current_value = decodeValueRaw();
}

void DecoderCA::createWindow(std::vector<std::string> & column, std::string previous_value){
    int previous_value_int = std::stoi(previous_value);
    int current_value_int = std::stoi(current_value);

    CAPoint first_point = CAPoint(0, previous_value_int);
    std::cout << "first_point = (0," << previous_value_int << ")" <<  std::endl;
    int last_point_time_delta = 0;
    for (int i=0; i < current_window_size; i++){ last_point_time_delta += time_delta_vector.at(row_index + i); }
    CAPoint last_point = CAPoint(last_point_time_delta, current_value_int);
    std::cout << "last_point = (" << last_point_time_delta << "," << current_value_int << ")" <<  std::endl;
    CALine line = CALine(first_point, last_point);

    int current_sum = 0;
    int time_delta = 0;

    for (int i=0; i < current_window_size; i++){
//        if (i > 0) { time_delta = time_delta_vector.at(row_index); }
        time_delta = time_delta_vector.at(row_index);
        current_sum += time_delta;

        std::cout << "current_sum = " << current_sum <<  std::endl;
        CAPoint point = CAPoint(current_sum, 0); // y doesn't matter
        double y = line.yIntersection(point);
        int val = std::round(y);
        std::string val_str = std::to_string(val);
        std::cout << "val_str = " << val_str <<  std::endl;
        column.push_back(val_str);
        row_index++;
        if (i == current_window_size - 1){
            assert(val == current_value_int);
        }
    }
}
