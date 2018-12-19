
#include "bit_stream_utils.h"

#include "bit_stream_reader.h"
#include <iostream>
#include <stdio.h>

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

    int cont=1; // first different bit
    bool diff = false;

    while (!reader1->reachedEOF()){
        if (reader2->reachedEOF()) { diff = true; break; }
        if (reader1->getInt(8)!=reader2->getInt(8)) { diff = true; break; }
        cont++;
    }
    if (!diff && !reader2->reachedEOF()) { diff = true; }

    delete reader1;
    delete reader2;

    cont = (diff ? cont : 0);
    return cont;
}

void BitStreamUtils::printBytes(Path path){
    std::cout << "printBytes " << path.full_path << std::endl;
    BitStreamReader* reader=new BitStreamReader(path);
    int cont = 1;
    int byte;
    while (!reader->reachedEOF()){
        byte = reader->getInt(8);
        std::cout << cont << " - " << byte << std::endl;
        cont++;
    }
    delete reader;
}

void BitStreamUtils::removeFile(Path path){
    const char * file_path = path.full_path.c_str();
    remove(file_path);
}
