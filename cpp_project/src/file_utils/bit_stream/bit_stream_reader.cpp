
#include "bit_stream_reader.h"
#include <iostream>

void BitStreamReader::construct(const char * file){
    fp = fopen(file, "rb");
    if (fp == NULL){
        std::string error_msg = "ERROR opening file ";
        throw std::runtime_error(error_msg + file);
    }
    offset = 0;
#if DEBUG
    current_byte = 0;
#endif
    read();
}

BitStreamReader::BitStreamReader(Path path){
    construct(path.full_path.c_str());
}

void BitStreamReader::read(){
    current = (unsigned char)fgetc(fp);
    current_unread = true;
}

int BitStreamReader::getBit(){
    if (current_unread){
        std::cout << "          (" << current_byte << ") read = " << int(current) << std::endl;
#if DEBUG
        current_byte++;
        if (current_byte > 100) exit(1);
#endif
    }
    current_unread = false;
    int ans = !!(current & (1 << offset) );
    offset = (offset + 1) & 7; // 0111

    if (offset == 0){
        read();
        if ( feof(fp) )
            current = 0;
    }
    return ans;
}

//int BitStreamReader::getBitOther(){
//    if (current_unread){
//        std::cout << "          (" << current_byte << ") read = " << int(current) << std::endl;
//#if DEBUG
//        current_byte++;
//        if (current_byte > 100) exit(1);
//#endif
//    }
//    current_unread = false;
//
//
//}

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

int BitStreamReader::getInt(){
    Integer my_int;
    // receive bytes and assign them to the union bytes
    for (int i=0; i < sizeof(int); i++){
        my_int.m_bytes[i] = getInt(8);
    }
    // get the float back from the union
    return my_int.m_int;
}

void BitStreamReader::flushByte(){
    if (current_unread) return;
    while (offset > 0){
        getBit();
    }
}

bool BitStreamReader::reachedEOF(){
    return feof(fp);
}

BitStreamReader::~BitStreamReader(){
    fclose(fp);
}
