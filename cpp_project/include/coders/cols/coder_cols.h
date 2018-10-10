
#ifndef CPP_PROJECT_CODER_COLS_H
#define CPP_PROJECT_CODER_COLS_H

#include "coder_base.h"
#include "dataset.h"

class CoderCols: public CoderBase {

private:
    void codeDataRows() override;

    void goToFirstDataRow();
    void codeColumn();

    virtual void codeColumnBefore() = 0;
    virtual void codeColumnWhile(std::string csv_value) = 0;
    virtual void codeColumnAfter() = 0;

protected:
    int column_index = 0;
    int row_index = 0;
    int delta_sum;
    std::vector<int> time_delta_vector;

#if MASK_MODE
    int total_data_rows;
#endif

    void codeDataColumn();
    void codeTimeDeltaColumn();

public:
    using CoderBase::CoderBase;
};

#endif //CPP_PROJECT_CODER_COLS_H
