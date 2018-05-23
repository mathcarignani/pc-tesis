
#ifndef CPP_PROJECT_BIT_STREAM_WRITER_H
#define CPP_PROJECT_BIT_STREAM_WRITER_H

#include <stdio.h>
#include <string>
#include "path.h"


class BitStreamWriter {

private:
    FILE * fp;
    unsigned char current, offset;
    void construct(const char * file);

public:
    BitStreamWriter();
    BitStreamWriter(const char * file);
    BitStreamWriter(std::string path, std::string filename);
    BitStreamWriter(Path path);

    void pushBit(unsigned int bit);

    void pushInt(unsigned int x, int k);

    void close();

    ~BitStreamWriter();

};

#endif //CPP_PROJECT_BIT_STREAM_WRITER_H
