
#ifndef CPP_PROJECT_CODER_COLS_H
#define CPP_PROJECT_CODER_COLS_H

#include "coder_base.h"
#include "dataset.h"

class CoderCols: public CoderBase {

private:
    void codeDataRows() override;
    virtual void codeColumn() = 0;
//    void createWindow();
protected:
    Dataset dataset;
    int column_index = 0;
    int row_index = 0;

public:
    using CoderBase::CoderBase;
    void setDataset();
    //    virtual std::string getInfo() = 0;
};

#endif //CPP_PROJECT_CODER_COLS_H