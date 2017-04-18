#include <cstring>
#include <iostream>
#include <stdlib.h>

#include "csv_utils.h"

int main(int argc, char *argv[]){
  
  // imprimo entrada al main
  for(int i=0; i<argc; i++){
    std::cout << argv[i] << " ";
  }
  std::cout << std::endl << std::endl;

  CsvUtils::code_csv_unary();

  return 0;
}

