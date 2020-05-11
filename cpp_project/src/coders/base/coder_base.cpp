
#include "coder_base.h"


void CoderBase::codeCoderParams(){
    codeCoderParameters(Constants::CODER_BASE, 1);
}

void CoderBase::codeColumnBefore() {}

void CoderBase::codeColumnWhile(std::string csv_value){
#if MASK_MODE
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
#endif
//    std::cout << "codeValueRaw = " << csv_value << std::endl;
    codeValueRaw(csv_value);
}

void CoderBase::codeColumnAfter() {}
