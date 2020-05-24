
#ifndef CPP_PROJECT_CODER_COLS_H
#define CPP_PROJECT_CODER_COLS_H

#include "coder_common.h"
#include "dataset.h"

class CoderCols: public CoderCommon {

private:
    void codeDataRows() override;

    void codeColumn();

    virtual void codeColumnBefore() = 0;
    virtual void codeColumnWhile(std::string csv_value) = 0;
    virtual void codeColumnAfter() = 0;

protected:
    int column_index = 0;
    int row_index = 0;
    int delta_sum = 0;
    std::vector<int> time_delta_vector;
#if MASK_MODE
    int total_data_rows;
#if MASK_MODE == 3
    std::vector<int> total_data_rows_vector;
#endif // MASK_MODE == 3
#endif // MASK_MODE

    void codeDataColumn();

public:
    using CoderCommon::CoderCommon;
};

#endif //CPP_PROJECT_CODER_COLS_H
