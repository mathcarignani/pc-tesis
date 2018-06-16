
#include "decoder_pwlh.h"

#include "string_utils.h"
#include "pwlh_window.h"
#include <cfloat>

void DecoderPWLH::setCoderParams(int max_window_size_, bool integer_mode_){
    max_window_size_bit_length = StringUtils::bitLength(max_window_size_);
    integer_mode = integer_mode_;
}

std::vector<std::string> DecoderPWLH::decodeColumn(){
    std::vector<std::string> column;
    row_index = 0;
    decodeWindow(column);
    while (row_index < data_rows_count){
        decodeWindow(column);
    }
    return column;
}

void DecoderPWLH::decodeWindow(std::vector<std::string> & column){
    int window_size = input_file.getInt(max_window_size_bit_length);
    if (integer_mode) { decodeWindowInt(column, window_size); } else { decodeWindowDouble(column, window_size); }
}

void DecoderPWLH::decodeWindowDouble(std::vector<std::string> & column, int window_size){
    //    std::cout << "WINDOW SIZE = " << window_size << std::endl;
    float value = decodeFloat();
    if (value == FLT_MAX){
        for (int i=0; i < window_size; i++){
//            std::cout << "OUTPUT >>>>>>>>>>>>>>>> " << "N" << std::endl;
            column.push_back("N");
            row_index++;
        }
    }
    else if (window_size > 1) {
        float point1_y = value;
        float point2_y = decodeFloat();
//        std::cout << "point1_y = " << point1_y << std::endl;
//        std::cout << "point2_y = " << point2_y << std::endl;

        std::vector<std::string> decoded_points = PWLHWindow::decodePoints(point1_y, point2_y, window_size);
        for (int i=0; i < window_size; i++){
            std::string decoded_point = decoded_points[i];
//            std::cout << "OUTPUT >>>>>>>>>>>>>>>> " << decoded_point << std::endl;
            column.push_back(decoded_point);
            row_index++;
        }
    }
    else { // window_size == 1 => this code can only run the last time decodeWindow is called
        int value_int = static_cast<int>(value);
        std::string value_str = std::to_string(value_int);
        column.push_back(value_str);
        row_index++;
    }
}

void DecoderPWLH::decodeWindowInt(std::vector<std::string> & column, int window_size){
//    std::cout << "WINDOW SIZE = " << window_size << std::endl;
    std::string value = decodeValueRaw();
    if (value == "N"){
        for (int i=0; i < window_size; i++){
//            std::cout << "OUTPUT >>>>>>>>>>>>>>>> " << "N" << std::endl;
            column.push_back(value);
            row_index++;
        }
    }
    else if (window_size > 1) {
        std::string point1_y = value;
        std::string point2_y = decodeValueRaw();
//        std::cout << "point1_y = " << point1_y << std::endl;
//        std::cout << "point2_y = " << point2_y << std::endl;

        std::vector<std::string> decoded_points = PWLHWindow::decodePointsIntegerMode(point1_y, point2_y, window_size);
        for (int i=0; i < window_size; i++){
            std::string decoded_point = decoded_points[i];
//            std::cout << "OUTPUT >>>>>>>>>>>>>>>> " << decoded_point << std::endl;
            column.push_back(decoded_point);
            row_index++;
        }
    }
    else { // window_size == 1 => this code can only run the last time decodeWindow is called
        column.push_back(value);
        row_index++;
    }
}
