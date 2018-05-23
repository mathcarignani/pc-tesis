
#ifndef CPP_PROJECT_BIT_STREAM_READER_H
#define CPP_PROJECT_BIT_STREAM_READER_H

#include <stdio.h>
#include <string>
#include "path.h"


class BitStreamReader {

private:
    FILE* fp;
    unsigned char current, offset;
    void construct(const char * file);

public:
    BitStreamReader();
    BitStreamReader(const char * file);
    BitStreamReader(std::string path, std::string filename);
    BitStreamReader(Path path);

    int getBit();

    unsigned int getInt(int bits);

    bool reachedEOF();

    ~BitStreamReader();

};

#endif //CPP_PROJECT_BIT_STREAM_READER_H
