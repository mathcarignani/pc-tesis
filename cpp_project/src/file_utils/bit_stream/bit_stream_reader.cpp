
#include "bit_stream_reader.h"
#include <iostream>

void BitStreamReader::construct(const char * file){
    fp = fopen(file, "rb");
    if (fp == NULL){
        std::string error_msg = "ERROR opening file ";
        throw std::runtime_error(error_msg + file);
    }
    offset = 0;
    current = (unsigned char)getc(fp);
}

BitStreamReader::BitStreamReader(Path path){
    construct(path.full_path.c_str());
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

float BitStreamReader::getFloat(){
    Float my_float;
    // receive bytes and assign them to the union bytes
    for (int i=0; i < sizeof(float); i++){
        my_float.m_bytes[i] = getInt(8);
    }
    // get the float back from the union
    return my_float.m_float;
}

double BitStreamReader::getDouble(){
    Double my_double;
    // receive bytes and assign them to the union bytes
    for (int i=0; i < sizeof(double); i++){
        my_double.m_bytes[i] = getInt(8);
    }
    // get the float back from the union
    return my_double.m_double;
}

bool BitStreamReader::reachedEOF(){
    return feof(fp);
}

BitStreamReader::~BitStreamReader(){
    fclose(fp);
}
