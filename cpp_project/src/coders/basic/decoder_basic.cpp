
#include "decoder_basic.h"
#include "assert.h"

std::vector<std::string> DecoderBasic::decodeDataColumn(){
    std::vector<std::string> column;
    row_index = 0;

#if MASK_MODE && CHECKS
    assert(mask->total_no_data + mask->total_data == data_rows_count);
#endif

    while (row_index < data_rows_count) {
    #if MASK_MODE
        if (mask->isNoData()) {
            column.push_back(Constants::NO_DATA);
            row_index++;
            continue;
        }
    #endif
        std::string value = decodeValueRaw();
        column.push_back(value);
        row_index++;
    }
    return column;
}
