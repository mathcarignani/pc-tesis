#include <iostream>
#include "csv_utils.h"
#include "minicsv.h"

// struct Product
// {
//     Product() : name(""), qty(0), price(0.0f) {}
//     Product(std::string name_, int qty_, float price_) 
//         : name(name_), qty(qty_), price(price_) {}
//     std::string name;
//     int qty;
//     float price;
// };

 // Year  Month   Day   Latitude  Longitude   Air Temp  Sea Surface Temp
 //  80    3      7      -0.02     -109.46     26.14       26.24


struct NinoRow
{
    NinoRow() : year(0), month(0), day(0), lat(0.0f), longi(0.0f), air_temp(0.0f), sea_temp(0.0f) {}
    NinoRow(int year_, int month_, int day_, float lat_, float longi_, float air_temp_, float sea_temp_)
        : year(year_), month(month_), day(day_), lat(lat_), longi(longi_), air_temp(air_temp_), sea_temp(sea_temp_) {}
    int year;
    int month;
    int day;
    float lat;
    float longi;
    float air_temp;
    float sea_temp;
};

template<>
inline mini::csv::ifstream& operator >> (mini::csv::ifstream& istm, NinoRow& val)
{
    return istm >> val.year >> val.month >> val.day >> val.lat >> val.longi >> val.air_temp >> val.sea_temp;
}

template<>
inline mini::csv::ostringstream& operator << (mini::csv::ostringstream& ostm, const NinoRow& val)
{
    return ostm << val.year; // << val.qty << val.price;
}

void CsvUtils::code_csv_unary(){
  mini::csv::ifstream is("elnino-clean.csv");
  is.set_delimiter(',', "$$");
  int line = 0;
  if(is.is_open())
  {
    NinoRow r;

    while(is.read_line())
    {
      line++;
      if (line == 1) { continue; } // skip column names
      is >> r;
      // display the read items
      std::cout << r.year << "|" << r.month << "|" << r.day << "|" << r.lat << "|" << r.longi << "|" << r.air_temp << "|" << r.sea_temp << std::endl;

      line++;
    }
  }
}
