
#include "csv_utils.h"

#include <iostream>

#include "bit_stream.h"
#include "minicsv.h"
#include "operation_utils.h"

// Year  Month   Day   Latitude  Longitude   Air Temp  Sea Surface Temp
//  80    3      7      -0.02     -109.46     26.14       26.24

struct NinoRow
{
    NinoRow() : year(0), month(0), day(0), lat(""), longi("") {} //, air_temp(0.0f), sea_temp(0.0f) {}
    NinoRow(int year_, int month_, int day_, std::string lat_, std::string longi_) //, float air_temp_, float sea_temp_)
            : year(year_), month(month_), day(day_), lat(lat_), longi(longi_) {} //, air_temp(air_temp_), sea_temp(sea_temp_) {}
    int year;
    int month;
    int day;
    std::string lat;
    std::string longi;
    // float air_temp;
    // float sea_temp;
};

template<>
inline mini::csv::ifstream& operator >> (mini::csv::ifstream& istm, NinoRow& val)
{
    return istm >> val.year >> val.month >> val.day >> val.lat >> val.longi; //>> val.air_temp >> val.sea_temp;
}

// template<>
// inline mini::csv::ostringstream& operator << (mini::csv::ostringstream& ostm, const NinoRow& val)
// {
//     return ostm << val.year; // << val.qty << val.price;
// }


void CsvUtils::code_csv(std::string filename, std::string coded_filename)
{
    BitStreamWriter* coded_file;
    const char * c = coded_filename.c_str();
    coded_file=new BitStreamWriter((char*)c);

    mini::csv::ifstream is(filename);
    is.set_delimiter(',', "$$");
    if(is.is_open())
    {
        NinoRow r;
        while(is.read_line())
        {
            // std::cout << "hola";
            is >> r;

            // std::cout << r.year;

            int offset_year = r.year - 80;
            coded_file->pushInt(offset_year, 5);

            int offset_month = r.month - 1;
            coded_file->pushInt(offset_month, 4);

            int offset_day = r.day - 1;
            coded_file->pushInt(offset_day, 5);

            // std::cout << r.lat;
            float offset_lat = atof(r.lat.c_str()) + 8.81;
            int offset_lat_left = 0;
            int offset_lat_right = 0;
            OperationUtils::set_right_left(offset_lat, &offset_lat_left, &offset_lat_right);

            coded_file->pushInt(offset_lat_left, 5);
            coded_file->pushInt(offset_lat_right, 7);

            // std::cout << "hola";
            // std::cout << offset_lat_left;
            // std::cout << ' ';
            // std::cout << offset_lat_right;
            // exit(0);

            // float offset_long = r.long + 180;
        }
        is.close();
    }
}

void CsvUtils::decode_csv(std::string coded_filename, std::string decoded_filename)
{
    BitStreamReader* coded_file;
    const char * c = coded_filename.c_str();
    coded_file=new BitStreamReader((char*)c);

    mini::csv::ofstream os(decoded_filename);
    os.set_delimiter(',', "$$");
    if(os.is_open())
    {
        while (!coded_file->reachedEOF())
        {
            int offset_year = coded_file->getInt(5);
            int year = offset_year + 80;
            // std::cout << year;
            // std::cout << " ";

            int offset_month = coded_file->getInt(4);
            int month = offset_month + 1;
            // std::cout << month;
            // std::cout << " ";

            int offset_day = coded_file->getInt(5);
            int day = offset_day + 1;
            // std::cout << day;
            // std::cout << " ";

            float offset_lat_left = coded_file->getInt(5);
            float offset_lat_right = coded_file->getInt(7);
            // std::cout << offset_lat_left;
            // std::cout << " ";
            // std::cout << offset_lat_right;

            float lat = offset_lat_left + offset_lat_right/100 - 8.81;
            // std::cout << " ";
            // std::cout << offset_lat_right/100;
            os << year << month << day << lat << NEWLINE;
        }
    }
    os.flush();
}
