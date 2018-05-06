
#include "bit_stream.h"

// ####################################################################################################### //
// ######################################### BitStreamWriter ############################################# //
// ####################################################################################################### //

BitStreamWriter::BitStreamWriter(char * file){
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

// ####################################################################################################### //
// ######################################### BitStreamReader ############################################# //
// ####################################################################################################### //

BitStreamReader::BitStreamReader(char * file){
    fp = fopen(file, "rb");
    offset = 0;
    current = (unsigned char)getc(fp);
}

int BitStreamReader::getBit(){
    int ans = !!(current & (1 << offset) );
    offset = (offset + 1) & 7;

    if (offset == 0){
        current = (unsigned char)fgetc(fp);
        if ( feof(fp) )
            current = 0;
    }
    return ans;
}

unsigned int BitStreamReader::getInt(int bits){
    int ans = 0;
    for (int i = bits-1; i >= 0; i--)
        ans |= getBit() << i;
    return ans;
}

bool BitStreamReader::reachedEOF(){
    return feof(fp);
}

BitStreamReader::~BitStreamReader(){
    fclose(fp);
}
