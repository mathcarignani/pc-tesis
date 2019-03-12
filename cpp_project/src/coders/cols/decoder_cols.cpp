
#include "decoder_cols.h"
#include "assert.h"
#include "string_utils.h"
#include "mask_decoder.h"
#include "time_delta_decoder.h"

void DecoderCols::decodeDataRows(){
    std::vector<std::vector<std::string>> columns;
    int total_columns = dataset->data_columns_count + 1;
    for(column_index = 0; column_index < total_columns; column_index++) {
    #if COUT
        std::cout << "decode column_index " << column_index << std::endl;
    #endif
        dataset->setColumn(column_index);
        std::vector<std::string> column = decodeColumn();
        columns.push_back(column);
    }
    transposeMatrix(data_rows_count, columns, total_columns);
}

std::vector<std::string> DecoderCols::decodeColumn(){
    if (column_index == 0) {
        std::vector<std::string> vec = TimeDeltaDecoder::decode(this);
//        std::cout << "D1 >> decoder->flushByte();" << std::endl;
//        flushByte();
//        std::cout << "D1 >> decoder->flushByte();" << std::endl;
        return vec;
    }
#if MASK_MODE
    std::cout << "MaskCoder::decode();" << std::endl;

    mask = MaskDecoder::decode(this);
//    std::cout << "D1 >> decoder->flushByte();" << std::endl;
//    flushByte();
//    std::cout << "D1 >> decoder->flushByte();" << std::endl;
#endif
    std::cout << "decodeDataColumn();" << std::endl;

    std::vector<std::string> col = decodeDataColumn();
//    std::cout << "D2 >> decoder->flushByte();" << std::endl;
//    flushByte();
//    std::cout << "D2 >> decoder->flushByte();" << std::endl;

    return col;
}
