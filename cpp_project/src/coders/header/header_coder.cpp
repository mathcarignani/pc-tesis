
#include "coders/header/header_coder.h"

#include "assert.h"
#include "string_utils.h"
#include "datetime_utils.h"
#include "header_utils.h"


Dataset HeaderCoder::codeHeader(){
    std::cout << "CODING..." << std::endl;
    DatasetUtils dataset_utils = DatasetUtils("code");
    codeDatasetName(dataset_utils);
    codeTimeUnit(dataset_utils);
    codeFirstTimestamp();
    codeColumnNames();
    return Dataset();
}

void HeaderCoder::codeDatasetName(DatasetUtils & dataset_utils){
    // DATASET:|NOAA-SST
    std::vector<std::string> current_line = input_csv.readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "DATASET:");
    std::string dataset_name = StringUtils::removeLastChar(current_line[1]);
    int dataset_int = dataset_utils.codeDatasetName(dataset_name);
    output_file.pushInt(dataset_int, 4); // 4 bits for the dataset name
}


void HeaderCoder::codeTimeUnit(DatasetUtils & dataset_utils){
    // TIME UNIT:|seconds
    std::vector<std::string> current_line = input_csv.readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "TIME UNIT:");
    std::string time_unit_name = StringUtils::removeLastChar(current_line[1]);
    int time_unit_int = dataset_utils.codeTimeUnit(time_unit_name);
    output_file.pushInt(time_unit_int, 4); // 4 bits for the time unit
}

void HeaderCoder::codeFirstTimestamp(){
    // FIRST TIMESTAMP:|2017-01-01 00:00:00
    std::vector<std::string> current_line = input_csv.readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "FIRST TIMESTAMP:");
    std::string timestamp_str = StringUtils::removeLastChar(current_line[1]);
    long int seconds = codeTimestamp(timestamp_str);
    output_file.pushInt(seconds, 32); // 32 bits for the timestamp
}

long int HeaderCoder::codeTimestamp(std::string timestamp_str){
    std::tm timestamp_tm = DatetimeUtils::parseDate(timestamp_str, HeaderUtils::date_format());

    assert(DatetimeUtils::compareDates(HeaderUtils::start_date(), timestamp_tm) == 1);
    assert(DatetimeUtils::compareDates(timestamp_tm, HeaderUtils::end_date()) == 1);

    long int seconds = DatetimeUtils::datetimeToSecondsSince(HeaderUtils::start_date(), timestamp_tm);
    return seconds;
}

void HeaderCoder::codeColumnNames(){
    // Time Delta|T0N110W|T0N125W|T0N155W|...|T9N140W
}
