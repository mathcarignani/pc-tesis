
#include "bit_stream_utils.h"

#include "bit_stream_reader.h"
#include <iostream>

int BitStreamUtils::compare(std::string path1, std::string filename1, std::string path2, std::string filename2){
    std::string fullpath1 = path1 + "/" + filename1;
    std::string fullpath2 = path2 + "/" + filename2;

    BitStreamReader* reader1=new BitStreamReader(fullpath1.c_str());
    BitStreamReader* reader2=new BitStreamReader(fullpath2.c_str());

    int cont=1; // first different bit

    while (!reader1->reachedEOF()){
        if (reader2->reachedEOF()) return cont;
        if (reader1->getBit()!=reader2->getBit()) return cont;
        cont++;
    }
    if (!reader2->reachedEOF()) return cont;

    return 0;
}
