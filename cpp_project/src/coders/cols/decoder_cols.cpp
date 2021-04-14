
#include <utils/vector_utils.h>
#include "decoder_cols.h"
#include "assert.h"
#include "string_utils.h"
#include "arithmetic_mask_decoder.h"
#include "time_delta_decoder.h"

void DecoderCols::decodeDataRows(){
    int total_columns = dataset->data_columns_count + 1;

    std::vector<std::vector<std::string>> columns;
    std::vector<std::string> column;

    column_index = 0;
//#if !MASK_MODE
    column = decodeColumn();
    columns.push_back(column);
//#endif

#if MASK_MODE
    ArithmeticMaskDecoder* amd = new ArithmeticMaskDecoder(this, dataset->data_columns_count);
    masks_vector = amd->decode();
#endif // MASK_MODE

    for(column_index = 1; column_index < total_columns; column_index++) {
        std::vector<std::string> column = decodeColumn();
        VectorUtils::printStringVector(column);
        columns.push_back(column);
    }
    transposeMatrix(data_rows_count, columns, total_columns);
}

std::vector<std::string> DecoderCols::decodeColumn(){
#if COUT
    std::cout << "decode column_index " << column_index << std::endl;
#endif
    dataset->setColumn(column_index);
    if (column_index == 0) {
        std::vector<std::string> vec = TimeDeltaDecoder::decode(this);
        return vec;
    }
#if MASK_MODE
    mask = masks_vector.at(column_index - 1);
#endif // MASK_MODE
    std::vector<std::string> col = decodeDataColumn();
    return col;
}
