
#ifndef CPP_PROJECT_HEADER_UTILS_H
#define CPP_PROJECT_HEADER_UTILS_H

#include <string>
#include "bit_stream_reader.h"
#include "bit_stream_writer.h"
#include "csv_reader.h"
#include "csv_writer.h"
#include "dataset.h"


class HeaderUtils {

public:
    static Dataset codeHeader(CSVReader &csv_reader, BitStreamWriter output_file);
    static Dataset decodeHeader(BitStreamReader input_file, CSVWriter &output_csv);

private:
    const std::string DATE_FORMAT = "%Y-%m-%d %H:%M:%S"; // "2010-10-01 00:00:00"
    const std::string START_DATE = ""; // datetime.strptime("1900-01-01 00:00:00", DATE_FORMAT)
    const std::string END_DATE = ""; // datetime.strptime("2036-02-07 06:28:16", DATE_FORMAT)

    static void codeColumnNames(std::vector<std::string> column_names_array, BitStreamWriter output_file);
    static std::vector<std::string> decodeColumnNames(BitStreamReader input_file);
};

#endif //CPP_PROJECT_HEADER_UTILS_H
