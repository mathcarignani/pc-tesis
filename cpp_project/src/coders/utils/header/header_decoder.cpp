
#include "header_decoder.h"

#include "assert.h"
#include "string_utils.h"
#include "dataset_utils.h"
#include "header_utils.h"
#include <vector>

HeaderDecoder::HeaderDecoder(BitStreamReader* input_file_, CSVWriter* output_csv_){
    input_file = input_file_;
    output_csv = output_csv_;
}

Dataset* HeaderDecoder::decodeHeader(){
    DatasetUtils* dataset_utils = new DatasetUtils("decode");
    std::string dataset_name = decodeDatasetName(*dataset_utils);
    decodeTimeUnit(*dataset_utils);
    decodeFirstTimestamp();
    int data_columns_count = decodeColumnNames();

    std::vector<Range> ranges = dataset_utils->getRangeVector(dataset_name);
    Dataset* dataset = new Dataset(ranges, data_columns_count);
    return dataset;
}

std::string HeaderDecoder::decodeDatasetName(DatasetUtils & dataset_utils){
    int dataset_int = input_file->getInt(4); // 4 bits for the dataset name
    std::string dataset_name = dataset_utils.decodeDatasetName(dataset_int);
    std::vector<std::string> row = {"DATASET:", dataset_name};
    output_csv->writeRowDecoder(row);
    return dataset_name;
}

void HeaderDecoder::decodeTimeUnit(DatasetUtils & dataset_utils){
    int time_unit_int = input_file->getInt(4); // 4 bits for the time unit
    std::string time_unit_name = dataset_utils.decodeTimeUnit(time_unit_int);
    std::vector<std::string> row = {"TIME UNIT:", time_unit_name};
    output_csv->writeRowDecoder(row);
}
void HeaderDecoder::decodeFirstTimestamp(){
    long int seconds = input_file->getInt(32); // 32 bits for the timestamp
    std::string timestamp_str = decodeTimestamp(seconds);
    std::vector<std::string> row = {"FIRST TIMESTAMP:", timestamp_str};
    output_csv->writeRowDecoder(row);
}

std::string HeaderDecoder::decodeTimestamp(long int seconds){
    std::tm timestamp_tm = DatetimeUtils::mapSecondsToDatetime(HeaderUtils::start_date(), seconds);

    assert(DatetimeUtils::compareDates(HeaderUtils::start_date(), timestamp_tm) == 1);
    assert(DatetimeUtils::compareDates(timestamp_tm, HeaderUtils::end_date()) == 1);

    std::string timestamp_str = DatetimeUtils::datetimeToString(timestamp_tm, HeaderUtils::date_format());
    return timestamp_str;
}

int HeaderDecoder::decodeColumnNames(){
    int number_of_chars = 0;
    // decode the number of chars in unary code
    while (input_file->getBit() > 0) { number_of_chars++; }
    int zeros_count = number_of_chars % 8 + 8;
    for(int i = 0; i < zeros_count - 1; i++) { input_file->getBit(); } // 0 bit
    // decode the chars (each char uses 1 byte)
    std::string column_names = "";
    for(int i = 0; i < number_of_chars; i++){
        int char_as_int = input_file->getInt(8);
        char character = StringUtils::intToChar(char_as_int);
        column_names += character;
    }
    std::vector<std::string> row = StringUtils::splitByString(column_names, ",");
    int data_columns_count = row.size();
    row.insert(row.begin(), "Time Delta"); // add "Time Delta"
    output_csv->writeRowDecoder(row); // call writeRow instead of writeRowDecoder
    return data_columns_count;
}
