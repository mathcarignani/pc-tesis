
#include "column_code.h"

ColumnCode::ColumnCode(){

}

ColumnCode::ColumnCode(Range range_, int bits_) {
    range = range_;
    bits = bits_;
    offset = -range.begin;
    nan = offset + range.end + 1;
    total_bits = 0;
    total_mask_bits = 0;
}

void ColumnCode::addBits(int bits_, bool mask_mode){
    if (mask_mode) {
        total_mask_bits += bits_;
    }
    else {
        total_bits += bits_;
    }
}
