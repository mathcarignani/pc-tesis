
#ifndef CPP_PROJECT_DECODER_COLS_H
#define CPP_PROJECT_DECODER_COLS_H

#include "decoder_base.h"

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

#if MASK_MODE
    std::vector<bool> burst_is_no_data_vector;
    std::vector<int> burst_length_vector;
    int current_index;
    bool burst_is_no_data;
    int burst_length;
    int total_no_data; // number of "nodata" entries
    int total_data; // number of non-"nodata" entries

    bool isNoData();
#endif

public:
    using DecoderBase::DecoderBase;

};

#endif //CPP_PROJECT_DECODER_COLS_H
