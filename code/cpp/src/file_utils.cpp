#include "file_utils.h"

int FileUtils::compare(char* file1, char* file2){

  BitStreamReader* reader1=new BitStreamReader(file1);
  BitStreamReader* reader2=new BitStreamReader(file2);

  int cont=1; // first different bit

  while (!reader1->reachedEOF()){
    if (reader2->reachedEOF()) return cont;
    if (reader1->getBit()!=reader2->getBit()) return cont;
    cont++;
  }
  if (!reader2->reachedEOF()) return cont;
  
  return 0;
}

void FileUtils::unary_code(BitStreamWriter* file, int n){
  for (int i=0; i<n; i++)
    file->pushBit(0);
  file->pushBit(1);
}

int FileUtils::unary_decode(BitStreamReader* file){

  int unary=0;
  bool cont=true;

  while (cont){
    if (file->reachedEOF()){ // end of file, return -1
      unary=-1;
      cont=false;
    }
    else if (file->getBit()){ // read 1, return unary code
      cont=false;
    }
    else { // read 0, increment unary code
      unary++;
    }
  }

  return unary;
}
