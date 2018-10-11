
#ifndef CPP_PROJECT_DECODER_COLS_H
#define CPP_PROJECT_DECODER_COLS_H

#include "decoder_base.h"
#include "mask.h"
#include "column.h"

class DecoderCols: public DecoderBase {

private:
    void decodeDataRows() override;

    std::vector<std::string> decodeColumn();
    std::vector<std::string> decodeTimeDeltaColumn();
    void transposeMatrix(std::vector<std::vector<std::string>> columns, int total_columns);

    virtual std::vector<std::string> decodeDataColumn() = 0;

protected:
    int column_index = 0;
    int row_index = 0;
    std::vector<int> time_delta_vector;
    Column* column;

#if MASK_MODE
    Mask* mask;
#endif

public:
    using DecoderBase::DecoderBase;

};

#endif //CPP_PROJECT_DECODER_COLS_H
