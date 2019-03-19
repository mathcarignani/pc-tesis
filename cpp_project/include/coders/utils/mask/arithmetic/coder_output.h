
#ifndef CPP_PROJECT_OUTPUT_H
#define CPP_PROJECT_OUTPUT_H

#include "coder_base.h"

class CoderOutput {

private:
    BitStreamWriter* writer;

public:
    CoderOutput(BitStreamWriter* writer_);
    void put_bit(bool bit);
};

#endif //CPP_PROJECT_OUTPUT_H
