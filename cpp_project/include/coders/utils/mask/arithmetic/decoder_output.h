
#ifndef CPP_PROJECT_DECODER_OUTPUT_H
#define CPP_PROJECT_DECODER_OUTPUT_H

#include "mask.h"

class DecoderOutput {

private:
    Mask* mask;
    Burst* burst;
    int last_column_index; // index of the last masked column
    int data_rows_count;
    int column_index;
    int row_index;

    void setNextColumn(int col_index);
    void endCurrentColumn();

public:
    std::vector<Mask*> masks_vector;

    // variables used by decompressor.h
    bool reset_model;
    bool eof;

    DecoderOutput(int data_rows_count_, int first_column_index_, int last_column_index_);
    void putByte(int c);
};

#endif //CPP_PROJECT_DECODER_OUTPUT_H
