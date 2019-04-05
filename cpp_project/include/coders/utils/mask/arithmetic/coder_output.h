
#ifndef CPP_PROJECT_OUTPUT_H
#define CPP_PROJECT_OUTPUT_H

#include "coder_base.h"

class CoderOutput {

private:
    BitStreamWriter* writer;
    bool print_;

public:
    int bit_count;
    int byte_count;

    CoderOutput(BitStreamWriter* writer_);
    void put_bit(bool bit);
    void print();
};

#endif //CPP_PROJECT_OUTPUT_H
