
#include "decoder_output.h"
#include "constants.h"

DecoderOutput::DecoderOutput(int data_rows_count_, int first_column_index_, int last_column_index_){
    data_rows_count = data_rows_count_;
    last_column_index = last_column_index_;

    reset_model = false;
    eof = false;
    setNextColumn(first_column_index_);
}

void DecoderOutput::setNextColumn(int col_index){
    column_index = col_index;
#if COUT
    std::cout << "decode mask column_index " << column_index << std::endl;
#endif
    row_index = 0;
    mask = new Mask();
}

void DecoderOutput::endCurrentColumn(){
    mask->close();
    mask->reset();
    // mask->print(false);
#if CHECKS
    assert(mask->total_data + mask->total_no_data == data_rows_count);
#endif // CHECKS
    masks_vector.push_back(mask);
    if (column_index < last_column_index){
        setNextColumn(column_index + 1);
        reset_model = true;
    }
    else { // column_index == last_column_index
        std::cout << "masks_vector.size() = " << masks_vector.size() << std::endl;
        std::cout << "columns_count = " << last_column_index + 1 << std::endl;
    #if CHECKS
        assert(masks_vector.size() == last_column_index + 1);
    #endif
        eof = true;
    }
}

//
// PRE: !eof()
//
void DecoderOutput::putByte(int c){
    reset_model = false;
    bool nodata = c == 1;
    mask->add(nodata);
    // std::cout << "[" << row_index << "] >>>>>>>>>>>>>>>>>>> DecoderOutput = " << c << std::endl;
    row_index++;
    if (row_index == data_rows_count){
        endCurrentColumn();
    }
}
