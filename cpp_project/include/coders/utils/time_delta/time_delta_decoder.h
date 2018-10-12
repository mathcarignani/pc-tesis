
#ifndef CPP_PROJECT_TIME_DELTA_DECODER_H
#define CPP_PROJECT_TIME_DELTA_DECODER_H

#include "decoder_base.h"

class TimeDeltaDecoder {

public:
    static std::vector<std::string> decode(DecoderBase* decoder);
};

#endif //CPP_PROJECT_TIME_DELTA_DECODER_H
