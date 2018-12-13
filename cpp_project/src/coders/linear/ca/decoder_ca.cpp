
#include "decoder_ca.h"
#include "string_utils.h"
#include "math_utils.h"
#include <cmath>
#include <vector_utils.h>
#include "Line.h"
#include "coder_utils.h"
#include "line_utils.h"
#include "linear_coder_utils.h"

void DecoderCA::setCoderParams(int window_size_){
    window_size_bit_length = MathUtils::bitLength(window_size_);
}

std::vector<std::string> DecoderCA::decodeDataColumn(){
#if MASK_MODE
    column = new Column(data_rows_count, mask->total_data, mask->total_no_data);
#else
    column = new Column(data_rows_count);
#endif

    while (column->notFinished()){
    #if MASK_MODE
        if (mask->isNoData()) {
            column->addNoData();
            continue;
        }
    #endif
        decodeWindow();
    }
//    std::cout << "column" << std::endl;
#if CHECKS
    column->assertAfter();
#endif
    return column->column_vector;
}

void DecoderCA::decodeWindow(){
//    std::cout << "BEGIN decodeWindow" << std::endl;
    int window_size = input_file->getInt(window_size_bit_length);
    std::string value = decodeValueRaw();

#if !MASK_MODE
    if (value == Constants::NO_DATA){
        column->addDataXTimes(value, window_size);
        return;
    }
#endif
    if (window_size > 1){
        decodeValues(window_size, value);
    }
    else {
        // window_size == 1
        column->addData(value);
    }
    archived_value = value;
//    std::cout << "END decodeWindow" << std::endl;
}

void DecoderCA::decodeValues(int window_size, std::string value){
//    std::cout << "BEGIN decodeValues" << std::endl;
//    std::cout << "column->row_index " << column->row_index << std::endl;
#if !MASK_MODE
    // column->row_index - 1 is the index of the archived_value
    // column->row_index - 1 + current_window_size + 1 = column->row_index + current_window_size is the index of the
    // last value to be decoded by this method
    std::vector<int> x_coords = CoderUtils::createXCoordsVector(time_delta_vector, window_size + 1, column->row_index-1);
    std::vector<std::string> decoded_points = LineUtils::decodePointsString(archived_value, value, x_coords);
#if CHECKS
    assert(decoded_points.at(0) == archived_value); // the first decoded point is equal to archived_value...
    assert(x_coords.at(0) == 0);
#endif
    decoded_points.erase(decoded_points.begin()); // ...we must remove it

    column->addDataVector(decoded_points);
#else // MASK_MODE
    std::vector<int> x_coords_with_nodata = LinearCoderUtils::createXCoordsWithNoDataVectorCA(this, window_size + 1, column->row_index-1);
    std::vector<int> x_coords = VectorUtils::removeOccurrences(x_coords_with_nodata, -1); // remove nodata
    std::vector<std::string> decoded_points = LineUtils::decodePointsString(archived_value, value, x_coords);
//    VectorUtils::printIntVector(x_coords_with_nodata);
//    VectorUtils::printIntVector(x_coords);
//    VectorUtils::printStringVector(decoded_points);

#if CHECKS
    assert(decoded_points.at(0) == archived_value); // the first decoded point is equal to archived_value...
    assert(x_coords_with_nodata.at(0) == 0);
#endif
    decoded_points.erase(decoded_points.begin()); // ...we must remove it
    x_coords_with_nodata.erase(x_coords_with_nodata.begin());
    LinearCoderUtils::addPointsWithNoData(column, window_size, decoded_points, x_coords_with_nodata);
//    column->addDataVector(decoded_points);
#endif // !MASK_MODE
//    std::cout << "END decodeValues" << std::endl;
}
