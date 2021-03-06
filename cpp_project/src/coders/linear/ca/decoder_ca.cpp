
#include "decoder_ca.h"
#include "string_utils.h"
#include "math_utils.h"
#include <cmath>
#include <vector_utils.h>
#include "Line.h"
#include "coder_utils.h"
#include "line_utils.h"
#include "linear_coder_utils.h"

std::vector<std::string> DecoderCA::decodeDataColumn(bool mask_mode){
    decode_archived_value = true; // always decode an archived value before decoding a window
#if MASK_MODE
    column = new Column(data_rows_count, mask->total_data, mask->total_no_data);
#else
    column = new Column(data_rows_count);
#endif
    int nodata_sum = 0;
    while (column->notFinished()){
        int current_time_delta = time_delta_vector.at(column->row_index);
    #if MASK_MODE
        if (mask->isNoData()) {
            nodata_sum += current_time_delta;
            column->addNoData();
            continue;
        }
    #endif
        decode(nodata_sum, current_time_delta);
        nodata_sum = 0;
    }
#if CHECKS
    column->assertAfter();
#endif
    return column->column_vector;
}

void DecoderCA::decode(int nodata_sum, int current_time_delta) {
    if (decode_archived_value || (nodata_sum + current_time_delta == 0)) {
    #if MASK_MODE
        decodeArchivedValue();
        decode_archived_value = false;
    #else
        decode_archived_value = decodeArchivedValue();
    #endif
    } else {
        decodeWindow(nodata_sum);
        decode_archived_value = true;
    }
}

bool DecoderCA::decodeArchivedValue() {
    std::string value = decodeValueRaw();

#if !MASK_MODE
    if (value == Constants::NO_DATA){
        int window_size = decodeWindowLength();
//        if (column_index == 1){
//            std::cout << "codeInt(" << window_size << ", " << window_size_bit_length << ")" << std::endl;
//        }
        column->addDataXTimes(value, window_size);
        return true;
    }
#endif
    column->addData(value);
    archived_value = value;
    return false;
}

void DecoderCA::decodeWindow(int nodata_sum){
    std::string value = decodeValueRaw();
//    if (column_index == 1){
//        std::cout << "codeValueRaw(" << value << ")" << std::endl;
//    }

    int window_size = decodeWindowLength();
//    if (column_index == 1){
//        std::cout << "codeInt(" << window_size << ", " << window_size_bit_length << ")" << std::endl;
//    }

#if !MASK_MODE
    if (value == Constants::NO_DATA){
        column->addDataXTimes(value, window_size);
        return;
    }
#endif

#if MASK_MODE
    decodeValues(window_size, value, nodata_sum);
#else
    decodeValues(window_size, value);
#endif

}

#if MASK_MODE
void DecoderCA::decodeValues(int window_size, std::string value, int nodata_sum){
    std::vector<int> x_coords_with_nodata = LinearCoderUtils::createXCoordsVectorCA(this, window_size + 1, column->row_index-1, nodata_sum);
    std::vector<int> x_coords = VectorUtils::removeOccurrences(x_coords_with_nodata, -1); // remove nodata
    std::vector<std::string> decoded_points = LineUtils::decodePointsString(archived_value, value, x_coords);

#if CHECKS
    assert(decoded_points.at(0) == archived_value); // the first decoded point is equal to archived_value...
    assert(x_coords_with_nodata.at(0) == 0);
#endif
    decoded_points.erase(decoded_points.begin()); // ...we must remove it
    x_coords_with_nodata.erase(x_coords_with_nodata.begin());
    LinearCoderUtils::addPointsWithNoData(column, window_size, decoded_points, x_coords_with_nodata);
}
#else
void DecoderCA::decodeValues(int window_size, std::string value){
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
}
#endif // MASK_MODE



