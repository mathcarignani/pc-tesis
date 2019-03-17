
#include "coder_basic.h"


void CoderBasic::codeCoderParams(){
    codeCoderParameters(Constants::CODER_BASIC, 1);
}

void CoderBasic::codeColumnBefore() {}

void CoderBasic::codeColumnWhile(std::string csv_value){
#if MASK_MODE
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
#endif
//    std::cout << "codeValueRaw = " << csv_value << std::endl;
    codeValueRaw(csv_value);
}

void CoderBasic::codeColumnAfter() {}
