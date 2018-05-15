
#include "column_code.h"

ColumnCode::ColumnCode(){

}

ColumnCode::ColumnCode(Range range_, int bits_) {
    range = range_;
    bits = bits_;
    offset = -range.begin;
    nan = offset + range.end + 1;
    total_bits = 0;
}

void ColumnCode::addBits(int bits_){
    total_bits += bits_;
}
