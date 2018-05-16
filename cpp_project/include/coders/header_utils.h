
#ifndef CPP_PROJECT_HEADER_UTILS_H
#define CPP_PROJECT_HEADER_UTILS_H

#include <string>
#include "bit_stream_reader.h"
#include "bit_stream_writer.h"
#include "csv_reader.h"
#include "csv_writer.h"
#include "dataset.h"
#include "dataset_utils.h"
#include "datetime_utils.h"


class HeaderUtils {

public:
    static Dataset codeHeader(CSVReader &csv_reader, BitStreamWriter output_file);
    static Dataset decodeHeader(BitStreamReader input_file, CSVWriter &output_csv);

private:
    static std::string date_format() { return "%Y-%m-%d %H:%M:%S"; }; // "2010-10-01 00:00:00"
    static std::tm start_date() { return DatetimeUtils::parseDate("1900-01-01 00:00:00", date_format()); };
    static std::tm end_date() { return DatetimeUtils::parseDate("2036-02-07 06:28:16", date_format()); };

    static long int codeTimestamp(std::string timestamp_str);
    static std::string decodeTimestamp(long int seconds);

//    static void codeColumnNames(std::vector<std::string> column_names_array, BitStreamWriter output_file);
//    static std::vector<std::string> decodeColumnNames(BitStreamReader input_file);
};

#endif //CPP_PROJECT_HEADER_UTILS_H
