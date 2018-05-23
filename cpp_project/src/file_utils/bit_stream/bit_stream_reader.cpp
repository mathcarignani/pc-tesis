
#include "bit_stream_reader.h"

void BitStreamReader::construct(const char * file){
    fp = fopen(file, "rb");
    offset = 0;
    current = (unsigned char)getc(fp);
}

BitStreamReader::BitStreamReader(){}

BitStreamReader::BitStreamReader(const char * file){
    construct(file);
}

BitStreamReader::BitStreamReader(std::string path, std::string filename){
    std::string full_path = path + "/" + filename;
    construct(full_path.c_str());
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

bool BitStreamReader::reachedEOF(){
    return feof(fp);
}

BitStreamReader::~BitStreamReader(){
    fclose(fp);
}
