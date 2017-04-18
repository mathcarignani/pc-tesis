#include <iostream>
#include "csv_utils.h"
#include "minicsv.h"

void CsvUtils::code_csv_unary(){
  mini::csv::ifstream is("elnino-clean.csv");
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
  }
}
