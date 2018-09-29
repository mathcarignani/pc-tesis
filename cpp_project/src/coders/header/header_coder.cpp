
#include "header_coder.h"

#include "assert.h"
#include "string_utils.h"
#include "datetime_utils.h"
#include "header_utils.h"
#include "vector_utils.h"

HeaderCoder::HeaderCoder(CSVReader* input_csv_, BitStreamWriter* output_file_){
    input_csv = input_csv_;
    output_file = output_file_;
}

Dataset HeaderCoder::codeHeader(){
    DatasetUtils dataset_utils = DatasetUtils("code");
    std::string dataset_name = codeDatasetName(dataset_utils); // 0.5 byte
    codeTimeUnit(dataset_utils); // 0.5 byte
    codeFirstTimestamp(); // 4 bytes
    int data_columns_count = codeColumnNames();

    std::vector<Range> ranges = dataset_utils.getRangeVector(dataset_name);
    std::vector<int> bits = dataset_utils.getBitsVector(dataset_name);
    Dataset dataset = Dataset(ranges, bits, data_columns_count);
    return dataset;
}

std::string HeaderCoder::codeDatasetName(DatasetUtils & dataset_utils){
    // DATASET:|NOAA-SST
    std::vector<std::string> current_line = input_csv->readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "DATASET:");
    std::string dataset_name = StringUtils::removeLastChar(current_line[1]);
    int dataset_int = dataset_utils.codeDatasetName(dataset_name);
    output_file->pushInt(dataset_int, 4); // 4 bits for the dataset name
    return dataset_name;
}


void HeaderCoder::codeTimeUnit(DatasetUtils & dataset_utils){
    // TIME UNIT:|seconds
    std::vector<std::string> current_line = input_csv->readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "TIME UNIT:");
    std::string time_unit_name = StringUtils::removeLastChar(current_line[1]);
    int time_unit_int = dataset_utils.codeTimeUnit(time_unit_name);
    output_file->pushInt(time_unit_int, 4); // 4 bits for the time unit
}

void HeaderCoder::codeFirstTimestamp(){
    // FIRST TIMESTAMP:|2017-01-01 00:00:00
    std::vector<std::string> current_line = input_csv->readLineCSV();
    assert(current_line.size() == 2);
    assert(current_line[0] == "FIRST TIMESTAMP:");
    std::string timestamp_str = StringUtils::removeLastChar(current_line[1]);
    long int seconds = codeTimestamp(timestamp_str);
    output_file->pushInt(seconds, 32); // 32 bits for the timestamp
}

long int HeaderCoder::codeTimestamp(std::string timestamp_str){
    std::tm timestamp_tm = DatetimeUtils::stringToDatetime(timestamp_str, HeaderUtils::date_format());

    assert(DatetimeUtils::compareDates(HeaderUtils::start_date(), timestamp_tm) == 1);
    assert(DatetimeUtils::compareDates(timestamp_tm, HeaderUtils::end_date()) == 1);

    long int seconds = DatetimeUtils::mapDatetimeToSeconds(HeaderUtils::start_date(), timestamp_tm);
    return seconds;
}

int HeaderCoder::codeColumnNames(){
    // Time Delta|T0N110W|T0N125W|T0N155W|...|T9N140W
    std::vector<std::string> current_line = input_csv->readLineCSV();
    current_line.erase(current_line.begin()); // remove "Time Delta"
    int data_columns_count = current_line.size();
    std::string column_names_str = StringUtils::join(current_line, ",");
    int number_of_chars = column_names_str.size() - 1;
    int zeros_count = number_of_chars % 8 + 8;

//    std::cout << "number_of_chars = " << number_of_chars << std::endl;
//    std::cout << "zeros_count = " << zeros_count << std::endl;

    // code the number of chars in unary code
    for(int i=0; i < number_of_chars; i++) { output_file->pushBit(1); }
    for(int i=0; i < zeros_count; i++) { output_file->pushBit(0); }
    // code the chars (each char uses 1 byte)
    for(int i=0; i < number_of_chars; i++) {
        char character = column_names_str[i];
        int char_as_int = StringUtils::charToInt(character);
        output_file->pushInt(char_as_int, 8);
    }
    return data_columns_count;
}
