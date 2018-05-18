//
//#include "file_a.h"
//
//#include "bit_stream_reader.h"
//


//void FileUtils::unary_code(BitStreamWriter* file, int n){
//    for (int i=0; i<n; i++)
//        file->pushBit(0);
//    file->pushBit(1);
//}
//
//int FileUtils::unary_decode(BitStreamReader* file){
//
//    int unary=0;
//    bool cont=true;
//
//    while (cont){
//        if (file->reachedEOF()){ // end of file, return -1
//            unary=-1;
//            cont=false;
//        }
//        else if (file->getBit()){ // read 1, return unary code
//            cont=false;
//        }
//        else { // read 0, increment unary code
//            unary++;
//        }
//    }
//
//    return unary;
//}

