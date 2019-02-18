
#ifndef CPP_PROJECT_BIT_STREAM_READER_H
#define CPP_PROJECT_BIT_STREAM_READER_H

#include <stdio.h>
#include <string>
#include "path.h"


class BitStreamReader {

private:
    //
    // SOURCE: https://os.mbed.com/forum/helloworld/topic/2053/?page=1#comment-54746
    //
    union Float {
        float    m_float;
        uint8_t  m_bytes[sizeof(float)];
    };
    union Double {
        double   m_double;
        uint8_t  m_bytes[sizeof(double)];
    };
    union Integer {
        int   m_int;
        uint8_t  m_bytes[sizeof(int)];
    };

    FILE* fp;
    unsigned char current, offset;
    void construct(const char * file);

public:
    BitStreamReader(Path path);

    int getBit();

    unsigned int getInt(int bits);

    float getFloat();
    double getDouble();
    int getInt();

    bool reachedEOF();

    ~BitStreamReader();

};

#endif //CPP_PROJECT_BIT_STREAM_READER_H
