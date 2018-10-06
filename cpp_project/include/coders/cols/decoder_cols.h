
#ifndef CPP_PROJECT_DECODER_COLS_H
#define CPP_PROJECT_DECODER_COLS_H

#include "decoder_base.h"
#include "mask.h"
#include "coder_utils.h"

class DecoderCols: public DecoderBase {

private:
    void decodeDataRows() override;

    std::vector<std::string> decodeColumn();
    std::vector<std::string> decodeTimeDeltaColumn();
#if MASK_MODE
    void decodeDataColumnNoDataMask();
#endif
    void transposeMatrix(std::vector<std::vector<std::string>> columns, int total_columns);

    virtual std::vector<std::string> decodeDataColumn() = 0;

protected:
    int column_index = 0;
    int row_index = 0;
    std::vector<int> time_delta_vector;
    Column* column;

#if MASK_MODE
    Mask* mask;
    int total_data;
    int total_no_data;
    bool isNoData();
    void reset();
#endif

    std::vector<int> createXCoordsVector();

public:
    using DecoderBase::DecoderBase;

};

#endif //CPP_PROJECT_DECODER_COLS_H
