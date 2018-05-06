
#ifndef CPP_PROJECT_BIT_STREAM_H
#define CPP_PROJECT_BIT_STREAM_H

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


class BitStreamReader {

private:
    FILE* fp;
    unsigned char current, offset;

public:

    BitStreamReader(char * file);

    int getBit();

    unsigned int getInt(int bits);

    bool reachedEOF();

    ~BitStreamReader();

};

#endif //CPP_PROJECT_BIT_STREAM_H
