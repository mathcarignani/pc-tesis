
#ifndef CPP_PROJECT_BIT_STREAM_WRITER_H
#define CPP_PROJECT_BIT_STREAM_WRITER_H

#include <stdio.h>


class BitStreamWriter {

private:
    FILE * fp;
    unsigned char current, offset;

public:

    BitStreamWriter(char * file);

    void pushBit(unsigned int bit);

    void pushInt(unsigned int x, int k);

    void close();

    ~BitStreamWriter();

};

#endif //CPP_PROJECT_BIT_STREAM_WRITER_H
