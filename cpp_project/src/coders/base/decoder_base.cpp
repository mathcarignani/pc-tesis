
#include "decoder_base.h"
#include "assert.h"
#include "vector_utils.h"

std::vector<std::string> DecoderBase::decodeDataColumn(bool mask_mode){
    std::vector<std::string> column;
    row_index = 0;

#if MASK_MODE && CHECKS
    assert(mask->total_no_data + mask->total_data == data_rows_count);
#endif

    while (row_index < data_rows_count) {
    #if MASK_MODE
        if (mask->isNoData()) {
            // std::cout << "row_index = " << row_index << std::endl;
            column.push_back(Constants::NO_DATA);
            row_index++;
            continue;
        }
    #endif
        std::string value = decodeValueRaw();
        // std::cout << "row_index = " << row_index << " => decodeValueRaw = " << value << std::endl;
        column.push_back(value);
        row_index++;
    }
    // VectorUtils::printStringVector(column);
    return column;
}
