
#ifndef CPP_PROJECT_BIT_STREAM_READER_H
#define CPP_PROJECT_BIT_STREAM_READER_H

#include <stdio.h>


class BitStreamReader {

private:
    FILE* fp;
    unsigned char current, offset;

public:

    BitStreamReader(const char * file);

    int getBit();

    unsigned int getInt(int bits);

    bool reachedEOF();

    ~BitStreamReader();

};

#endif //CPP_PROJECT_BIT_STREAM_READER_H
