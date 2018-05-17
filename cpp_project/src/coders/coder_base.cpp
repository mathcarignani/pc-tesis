
#include "coder_base.h"

//#include <cstring>
#include <iostream>
//#include "bit_stream_writer.h"
//#include "csv_reader.h"
#include "coders/header/header_coder.h"


void CoderBase::codeDataRowsCount(){
    int data_rows_count = input_csv.total_lines - 4;
    output_file.pushInt(data_rows_count, 24); // 24 bits for the data rows count
}

//
// This method maps a value read in the csv file into an integer to be written in the output file.
// It also checks the minimum and maximum constraints.
//
int CoderBase::codeValue(std::string x, int row_index, int col_index){
//    if x == 'N':
//        return self.dataset.nan
//
//    x = int(x)
//    if self.dataset.min <= x <= self.dataset.max:
//        return x + self.dataset.offset
//
//    CoderBase.raise_range_error(self.dataset.min, self.dataset.max, x, row_index, col_index)
    return std::stoi(x);
}

void CoderBase::codeRaw(int value){
//    self.output_file.write_int(value, self.dataset.get_bits())
//    output_file.pushInt(value, 20);
}

void CoderBase::codeValueRaw(std::string x, int row_index, int col_index){
    int value = codeValue(x, row_index, col_index);
    codeRaw(value);
}

void CoderBase::raiseRangeError(){
//    #
//    # TODO: move this code to a utils module
//    #
//    @classmethod
//    def raise_range_error(cls, minimum, maximum, x, row_index, col_index):
//        error_str = ("ERROR: min = %s <= x = %s <= max = %s\n" % (minimum, x, maximum)) +\
//                        ("POSITION = [%s,%s]" % (row_index, col_index))
//        raise StandardError(error_str)
}

void CoderBase::codeFile(){
    dataset = HeaderCoder(input_csv, output_file).codeHeader();
    codeDataRowsCount();
//    codeDataRows();
}

void CoderBase::close(){
    input_csv.close();
    output_file.~BitStreamWriter();
}
