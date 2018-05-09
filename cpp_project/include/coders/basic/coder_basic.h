
#ifndef CPP_PROJECT_CODER_BASIC_H
#define CPP_PROJECT_CODER_BASIC_H

#include "coder_base.h"

class CoderBasic: public CoderBase {

private:
    void codeDataRows() override;

public:
    using CoderBase::CoderBase;
    std::string getInfo();

};
#endif //CPP_PROJECT_CODER_BASIC_H
