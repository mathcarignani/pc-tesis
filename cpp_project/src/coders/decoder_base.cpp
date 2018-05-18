
#include "decoder_base.h"

#include "header_decoder.h"


void DecoderBase::decodeDataRowsCount(){
    data_rows_count = input_file.getInt(24); // 24 bits for the data rows count
}

//void DecoderBase::decodeValue(std::string y, int row_index, int col_index);
//void DecoderBase::decodeRaw();
//void DecoderBase::decodeValueRaw(int row_index, int col_index);

void DecoderBase::decodeFile(){
    dataset = HeaderDecoder(input_file, output_csv).decodeHeader();
    decodeDataRowsCount();
}

void DecoderBase::close(){
    input_file.~BitStreamReader();
    output_csv.close();
}
