
#ifndef CPP_PROJECT_BIT_STREAM_WRITER_H
#define CPP_PROJECT_BIT_STREAM_WRITER_H

#include <stdio.h>
#include <string>
#include "path.h"


class BitStreamWriter {

private:
    //
    // SOURCE: https://os.mbed.com/forum/helloworld/topic/2053/?page=1#comment-54746
    //
    union Float {
        float    m_float;
        uint8_t  m_bytes[sizeof(float)];
    };

    FILE * fp;
    unsigned char current, offset;
    void construct(const char * file);

public:
    BitStreamWriter(Path path);

    void pushBit(unsigned int bit);

    void pushInt(unsigned int x, int k);

    void pushFloat(float x);

    void close();

    ~BitStreamWriter();

};

#endif //CPP_PROJECT_BIT_STREAM_WRITER_H
