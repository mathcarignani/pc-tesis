
#include "bit_stream_writer.h"


BitStreamWriter::BitStreamWriter(const char * file){
    fp = fopen(file,"w");
    current = 0, offset = 0;
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

void BitStreamWriter::close(){
    if (offset > 0)
        fputc(current,fp), offset = 0, current = 0;
    fclose(fp);
}

BitStreamWriter::~BitStreamWriter(){
    close();
}
