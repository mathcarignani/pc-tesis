
#include "coder_basic.h"


void CoderBasic::codeCoderParams(){
    codeCoderParameters(Constants::CODER_BASIC, 1);
}

void CoderBasic::codeColumnBefore() {}

void CoderBasic::codeColumnWhile(int value){
#if MASK_MODE
    if (Constants::isNoData(value)) { return; } // skip no_data
#endif
    std::cout << "codeValueRaw(" << value << ")" << std::endl;
    codeValueRaw(value);
}

void CoderBasic::codeColumnAfter() {}
