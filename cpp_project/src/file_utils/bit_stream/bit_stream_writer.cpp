
#include "bit_stream_writer.h"

#include <iostream>

void BitStreamWriter::construct(const char * file){
    fp = fopen(file,"w");
    current = 0, offset = 0;
}

BitStreamWriter::BitStreamWriter(){}

BitStreamWriter::BitStreamWriter(Path path){
    construct(path.full_path.c_str());
}

void BitStreamWriter::pushBit(unsigned int bit){
    if (bit > 0)  current |= 1 << offset;
    offset = (offset + 1) & 7;

    if (offset == 0){
        fputc(current,fp);
        current = 0;
    }
}

void BitStreamWriter::pushInt(unsigned int x, int k){
    for (int i = k-1; i >=0; i--)
        this->pushBit( !!(x & (1 << i) ) );
}

void BitStreamWriter::pushFloat(float x){
    Float my_float;
    my_float.m_float = x; // assign a float to union
    for (int i=0; i < sizeof(float); i++){
        pushInt(my_float.m_bytes[i], 8); // get the 4 bytes
    }
}

void BitStreamWriter::close(){
    if (offset > 0)
        fputc(current,fp), offset = 0, current = 0;
    fclose(fp);
}

BitStreamWriter::~BitStreamWriter(){
    close();
}
