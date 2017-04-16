#include <cstring>
#include <iostream>
#include <stdlib.h>
// using namespace std;

#include "minicsv.h"

int main(int argc, char *argv[]){
  
  // imprimo entrada al main
  for(int i=0; i<argc; i++){
    std::cout << argv[i] << " ";
  }
  std::cout << std::endl << std::endl;

  const std::string filename = "elnino-clean.csvdddd";

  mini::csv::ifstream is(filename, std::ios_base::in);
  is.set_delimiter(',', "$$");
  if(is.is_open())
  {
    std::string a = "";
    std::string b = "";
    std::string c = "";
    std::string d = "";
    std::string e = "";
    std::string f = "";
    std::string g = "";

    while(is.read_line())
    {
        is >> a >> b >> c >> d >> e >> f >> g;
        // display the read items
        std::cout << a << "|" << b << "|" << c << "|" << d << "|" << e << "|" << f << "|" << g << std::endl;
    }
      // Product temp;
      // while(is.read_line())
      // {
      //     is >> temp.name >> temp.qty >> temp.price;
      //     // display the read items
      //     std::cout << temp.name << "|" << temp.qty << "|" << temp.price << std::endl;
      // }
  }
  return 0;
}

