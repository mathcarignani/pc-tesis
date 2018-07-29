
#ifndef CPP_PROJECT_DECODER_COLS_H
#define CPP_PROJECT_DECODER_COLS_H

#include "decoder_base.h"

class DecoderCols: public DecoderBase {

private:
    void decodeDataRows() override;

    void decodeNoDataMask();
    std::vector<std::string> decodeColumn();
    std::vector<std::string> decodeTimeDeltaColumn();
    void transposeMatrix(std::vector<std::vector<std::string>> columns, int total_columns);

    virtual std::vector<std::string> decodeDataColumn() = 0;

protected:
    bool MASK_MODE = false;
    int column_index = 0;
    int row_index = 0;
    std::vector<int> time_delta_vector;

public:
    using DecoderBase::DecoderBase;

};

#endif //CPP_PROJECT_DECODER_COLS_H
