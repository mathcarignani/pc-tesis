
#include "decoder_basic.h"
#include "assert.h"

std::vector<std::string> DecoderBasic::decodeDataColumn(){
    std::vector<std::string> column;
    row_index = 0;

#if MASK_MODE
    assert(total_no_data + total_data == data_rows_count);
#endif

    while (row_index < data_rows_count) {
    #if MASK_MODE
        if (isNoData()) {
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
