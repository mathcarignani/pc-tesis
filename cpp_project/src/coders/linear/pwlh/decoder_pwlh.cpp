
#include "decoder_pwlh.h"

#include "math_utils.h"
#include "pwlh_window.h"
#include <cfloat>
#include <vector_utils.h>
#include "constants.h"
#include "string_utils.h"
#include "coder_utils.h"

void DecoderPWLH::setCoderParams(int max_window_size_, bool integer_mode_){
    max_window_size_bit_length = MathUtils::bitLength(max_window_size_);
    integer_mode = integer_mode_;
}

std::vector<std::string> DecoderPWLH::decodeDataColumn(){
#if MASK_MODE
    column = new Column(data_rows_count, total_data, total_no_data);
#else
    column = new Column(data_rows_count);
#endif

    while (column->unprocessed_rows > 0){
    #if MASK_MODE
        if (isNoData()) {
            column->addNoData();
            continue;
        }
    #endif
        decodeWindow();
    }

#if CHECKS
    column->assertAfter();
#endif
    return column->column_vector;
}

void DecoderPWLH::decodeWindow(){
    int window_size = input_file->getInt(max_window_size_bit_length);
    integer_mode ? decodeWindowInt(window_size) : decodeWindowDouble(window_size);
}

void DecoderPWLH::decodeWindowDouble(int window_size){
    float value = decodeFloat();
#if !MASK_MODE
    if (value == FLT_MAX){
        addNoDataPoints(window_size);
        return;
    }
#endif
    if (window_size > 1) {
        float point1_y = value;
        float point2_y = decodeFloat();
    #if !MASK_MODE
        std::vector<int> x_coords = CoderUtils::createXCoordsVector(time_delta_vector, window_size, column->row_index);
        std::vector<std::string> decoded_points = PWLHWindow::decodePoints(point1_y, point2_y, x_coords);
        addPoints(window_size, decoded_points);
    #else
        std::vector<int> x_coords_with_nodata = createXCoordsWithNoDataVector(window_size);
        std::vector<int> x_coords = VectorUtils::removeOccurrences(x_coords_with_nodata, -1); // remove nodata
        std::vector<std::string> decoded_points = PWLHWindow::decodePoints(point1_y, point2_y, x_coords);
        addPointsWithNoData(window_size, decoded_points, x_coords_with_nodata);
    #endif
        return;
    }
    // window_size == 1 => this code can only run the last time decodeWindow is called
    int value_int = static_cast<int>(value);
    std::string value_str = StringUtils::intToString(value_int);
    column->addData(value_str);
}

void DecoderPWLH::decodeWindowInt(int window_size){
    std::string value = decodeValueRaw();
#if !MASK_MODE
    if (value == Constants::NO_DATA){
        addNoDataPoints(window_size);
        return;
    }
#endif
    if (window_size > 1) {
        std::string point1_y = value;
        std::string point2_y = decodeValueRaw();
    #if !MASK_MODE
        std::vector<int> x_coords = CoderUtils::createXCoordsVector(time_delta_vector, window_size, column->row_index);
        std::vector<std::string> decoded_points = PWLHWindow::decodePointsIntegerMode(point1_y, point2_y, x_coords);
        addPoints(window_size, decoded_points);
    #else
        std::vector<int> x_coords_with_nodata = createXCoordsWithNoDataVector(window_size);
        std::vector<int> x_coords = VectorUtils::removeOccurrences(x_coords_with_nodata, -1); // remove nodata
        std::vector<std::string> decoded_points = PWLHWindow::decodePointsIntegerMode(point1_y, point2_y, x_coords);
        addPointsWithNoData(window_size, decoded_points, x_coords_with_nodata);
    #endif
        return;
    }
    // window_size == 1 => this code can only run the last time decodeWindow is called
    column->addData(value);
}

#if !MASK_MODE

void DecoderPWLH::addPoints(int window_size, std::vector<std::string> decoded_points){
    for (int i=0; i < window_size; i++){
        std::string decoded_point = decoded_points[i];
        column->addData(decoded_point);
    }
}

void DecoderPWLH::addNoDataPoints(int window_size){
    for (int i=0; i < window_size; i++){
        column->addNoData();
    }
}

#else

std::vector<int> DecoderPWLH::createXCoordsWithNoDataVector(int window_size){
    std::vector<int> result;
    int current_sum = 0;
    int time_delta;
    int window_index = 0;
    int time_delta_index = -1;
    while(window_index < window_size){
        time_delta_index++;
        time_delta = (time_delta_index == 0) ? 0 : time_delta_vector.at(column->row_index + time_delta_index);
        current_sum += time_delta;

        if (time_delta_index > 0 && isNoData()){
            // isNoData() is always false in the first iteration
            result.push_back(-1);
            continue;
        }
        result.push_back(current_sum);
        window_index++;
    }
    return result;
}

void DecoderPWLH::addPointsWithNoData(int window_size, std::vector<std::string> decoded_points, std::vector<int> x_coords_with_nodata){
#if CHECKS
    assert(window_size == decoded_points.size());
    assert(window_size <= x_coords_with_nodata.size());
#endif
    int i = -1;
    int window_index = 0;
    while (window_index < window_size){
        i++;
        if (x_coords_with_nodata[i] == -1){
            column->addNoData();
            continue;
        }
        std::string decoded_point = decoded_points[window_index];
        column->addData(decoded_point);
        window_index++;
    }
}

#endif
