
#include "bit_stream_utils.h"

#include "bit_stream_reader.h"
#include <iostream>

int BitStreamUtils::compare(Path path1, Path path2){
    BitStreamReader* reader1=new BitStreamReader(path1);
    BitStreamReader* reader2=new BitStreamReader(path2);

    int cont=1; // first different bit

    while (!reader1->reachedEOF()){
        if (reader2->reachedEOF()) return cont;
        if (reader1->getBit()!=reader2->getBit()) return cont;
        cont++;
    }
    if (!reader2->reachedEOF()) return cont;

    return 0;
}

int BitStreamUtils::compareBytes(Path path1, Path path2){
    BitStreamReader* reader1=new BitStreamReader(path1);
    BitStreamReader* reader2=new BitStreamReader(path2);

    int byte_count=1; // first different byte

    while (!reader1->reachedEOF()){
        if (reader2->reachedEOF()) return byte_count;
        unsigned int reader1_byte = reader1->getInt(8);
        unsigned int reader2_byte = reader2->getInt(8);
//        std::cout << "byte " << byte_count << " " << reader1_byte << " " << reader2_byte << std::endl;
        if (reader1_byte!=reader2_byte) return byte_count;
//        if (byte_count == 100) { return byte_count; }
        byte_count++;
    }
    if (!reader2->reachedEOF()) return byte_count;

    return 0;
}


