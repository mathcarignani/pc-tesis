
#ifndef CPP_PROJECT_CODER_COLS_H
#define CPP_PROJECT_CODER_COLS_H

#include "coder_base.h"
#include "dataset.h"

class CoderCols: public CoderBase {

private:
    void codeDataRows() override;

    void codeNoDataMask();
    void codeColumn();
    void codeTimeDeltaColumn();
    void codeDataColumn();

    virtual void codeColumnBefore() = 0;
    virtual void codeColumnWhile(std::string csv_value) = 0;
    virtual void codeColumnAfter() = 0;

protected:
    bool MASK_MODE = false;
    int column_index = 0;
    int row_index = 0;
    std::vector<int> time_delta_vector;

public:
    using CoderBase::CoderBase;

};

#endif //CPP_PROJECT_CODER_COLS_H
