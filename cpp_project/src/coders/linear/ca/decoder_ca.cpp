
#include "decoder_ca.h"

#include "string_utils.h"
#include "ca_line.h"
#include <cmath>

void DecoderCA::setCoderParams(int max_window_size_){
    max_window_size_bit_length = StringUtils::bitLength(max_window_size_);
}


std::vector<std::string> DecoderCA::decodeDataColumn(){
    std::vector<std::string> column;
    std::string archived_value = "random"; // any value that cannot be read from the csv
    row_index = 0;

//    std::cout << "row_index = " << row_index << std::endl;

    while (row_index < data_rows_count){
//        std::cout << "row_index = " << row_index << std::endl;
        decodeWindow(column);

        if (current_window_size == 1){
//            std::cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PUSH = " << current_value <<  std::endl;
            column.push_back(current_value);
            row_index++;
        }
        else if (current_value == Constants::NO_DATA){
            for (int i=0; i < current_window_size; i++){
//                std::cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PUSH = " << current_value <<  std::endl;
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
    current_window_size = input_file.getInt(max_window_size_bit_length);
    current_value = decodeValueRaw();
//    std::cout << "current_window_size = " << current_window_size << ", current_value = " << current_value << std::endl;
}

void DecoderCA::createWindow(std::vector<std::string> & column, std::string archived_value){
//    std::cout << "archived_value = " << archived_value << ", current_value = " << current_value << std::endl;
    int archived_value_int = StringUtils::stringToInt(archived_value);
    int current_value_int = StringUtils::stringToInt(current_value);

    CAPoint first_point = CAPoint(0, archived_value_int);
//    std::cout << "first_point = (0," << archived_value_int << ")" <<  std::endl;
    int last_point_time_delta = 0;
    for (int i=0; i < current_window_size; i++){ last_point_time_delta += time_delta_vector.at(row_index + i); }
    CAPoint last_point = CAPoint(last_point_time_delta, current_value_int);
//    std::cout << "last_point = (" << last_point_time_delta << "," << current_value_int << ")" <<  std::endl;
    CALine line = CALine(first_point, last_point);

    int current_sum = 0;
    int time_delta = 0;

    for (int i=0; i < current_window_size; i++){
//        if (i > 0) { time_delta = time_delta_vector.at(row_index); }
        time_delta = time_delta_vector.at(row_index);
//        std::cout << "time_delta = " << time_delta <<  std::endl;
        if (i > 0) { assert(time_delta > 0); }
        current_sum += time_delta;

//        std::cout << "current_sum = " << current_sum <<  std::endl;
        CAPoint point = CAPoint(current_sum, 0); // y doesn't matter
        double y = line.yIntersection(point);
        int val = std::round(y);
        std::string val_str = std::to_string(val);
//        std::cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PUSH = " << val_str <<  std::endl;
        column.push_back(val_str);
        row_index++;
        if (i == current_window_size - 1){
            assert(val == current_value_int);
        }
    }
}
