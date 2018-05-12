
#ifndef CPP_PROJECT_CODER_COLS_H
#define CPP_PROJECT_CODER_COLS_H

#endif //CPP_PROJECT_CODER_COLS_H

#include "coder_base.h"

class CoderCols: public CoderBase {

private:
    void codeDataRows() override;
    virtual void codeColumn() = 0;
//    void createWindow();
protected:
    int column_index = 0;
    int row_index = 0;

public:
    using CoderBase::CoderBase;
    //    virtual std::string getInfo() = 0;
};



//class CoderBasic: public CoderBase {
//
//private:
//    void codeDataRows() override;
//
//public:
//    using CoderBase::CoderBase;
//    std::string getInfo();
//
//};