
#include "header_utils.h"

#include "assert.h"
#include <vector>


Dataset HeaderUtils::codeHeader(CSVReader &csv_reader, BitStreamWriter output_file){
    std::cout << "CODING..." << std::endl;
    DatasetUtils dataset_utils = DatasetUtils("code");
    std::vector<std::string> current_line;

    // DATASET:|NOAA-SST
    current_line = csv_reader.readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "DATASET:");
    std::string dataset_name = current_line[1];
    int dataset_int = dataset_utils.codeDatasetName(dataset_name);
    output_file.pushInt(dataset_int, 4); // 4 bits for the dataset name

    // TIME UNIT:|seconds
    current_line = csv_reader.readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "TIME UNIT:");
    std::string time_unit_name = current_line[1];
    int time_unit_int = dataset_utils.codeTimeUnit(time_unit_name);
    output_file.pushInt(time_unit_int, 4); // 4 bits for the time unit

    // FIRST TIMESTAMP:|2017-01-01 00:00:00
    current_line = csv_reader.readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "FIRST TIMESTAMP:");
    std::string timestamp_str = current_line[1];
    long int seconds = codeTimestamp(timestamp_str);
    std::cout << "code seconds " << seconds << std::endl;
    output_file.pushInt(seconds, 32); // 32 bits for the timestamp

    // Time Delta|T0N110W|T0N125W|T0N155W|...|T9N140W

    return Dataset();
}

long int HeaderUtils::codeTimestamp(std::string timestamp_str){
    std::tm timestamp_tm = DatetimeUtils::parseDate(timestamp_str, date_format());

    assert(DatetimeUtils::compareDates(start_date(), timestamp_tm) == 1);
    assert(DatetimeUtils::compareDates(timestamp_tm, end_date()) == 1);

    long int seconds = DatetimeUtils::datetimeToSecondsSince(start_date(), timestamp_tm);
    return seconds;
}




Dataset HeaderUtils::decodeHeader(BitStreamReader input_file, CSVWriter &output_csv){
    std::cout << "DECODING..." << std::endl;
    DatasetUtils dataset_utils = DatasetUtils("decode");

    int dataset_int = input_file.getInt(4); // 4 bits for the dataset name
    std::string dataset_name = dataset_utils.decodeDatasetName(dataset_int);
    std::vector<std::string> row = {"DATASET:", dataset_name};
    output_csv.writeRow(row);

    int time_unit_int = input_file.getInt(4); // 4 bits for the time unit
    std::string time_unit_name = dataset_utils.decodeTimeUnit(time_unit_int);

//    long int seconds = input_file.getInt(32); // 32 bits for the timestamp
//    std::string time_unit_name = dataset_utils.decodeTimeUnit(time_unit_int);

    return Dataset();
}

std::string HeaderUtils::decodeTimestamp(long int seconds){
//    assert(action == "decode");


}