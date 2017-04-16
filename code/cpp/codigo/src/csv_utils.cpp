#include "csv_utils.h"
#include "minicsv.h"
using namespace std;

void CsvUtils::code_csv_unary(){
  // open csv file
  // iterate through the first row_count rows
  mini::csv::ifstream is("elnino-clean.csv", std::ios_base::in);
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

// void CsvUtils::decode_csv_unary(int row_count, char* input_file, char* output_file){
  
// }
