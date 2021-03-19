
#include "dataset_utils.h"

#include "assert.h"
#include "string_utils.h"
#include "conversor.h"
#include <math.h>
#include "vector_utils.h"

const std::vector<std::string> DatasetUtils::DATASET_NAMES = {"IRKIS"};

const int DatasetUtils::MAX_DATA_ROWS_BITS = 24;
const int DatasetUtils::MAX_COLUMN_BITS = 10;

const std::vector<std::string> DatasetUtils::UNITS = {"minutes", "dimensionless"};

const std::vector<int> DatasetUtils::SCALES = {1, 10, 100, 1000};

const std::string DatasetUtils::METADATA_HEADER = "METADATA:";
const std::string DatasetUtils::METADATA_COLUMNS = "COLUMNS,UNIT,SCALE,MINIMUM,MAXIMUM";
const std::string DatasetUtils::DATA_HEADER = "DATA:";

bool DatasetUtils::validDatasetName(std::string dataset_name){
    return VectorUtils::vectorIncludesString(DATASET_NAMES, dataset_name);
}

bool DatasetUtils::validDataRowsCount(int data_rows_count){
    int max_data_rows = pow(2, MAX_DATA_ROWS_BITS);
    return (0 < data_rows_count && data_rows_count < max_data_rows);
}

bool DatasetUtils::validUnit(std::string unit){
    return VectorUtils::vectorIncludesString(UNITS, unit);
}

bool DatasetUtils::validScale(std::string scale){
    int scale_int = Conversor::stringToInt(scale);
    return VectorUtils::vectorIncludesInt(SCALES, scale_int);
}

// TODO: remove
DatasetUtils::DatasetUtils(std::string action_){
    assert(action_ == "code" || action_ == "decode");
    action = action_;
    input_file = new TextReader(PATH, FILENAME);
}

std::string DatasetUtils::findLine(std::string string_group, std::string string_to_find){
    input_file->goToLine(0);
    assert(input_file->findLine(string_group));
    assert(input_file->findLine(string_to_find));
    return input_file->current_line;
}

int DatasetUtils::codeDatasetName(std::string dataset_name){
    assert(action == "code");
    std::string line = findLine(DATASET_KEY, dataset_name);
    return Conversor::stringToInt(StringUtils::splitByString(line, SEPARATOR)[1]);
}

int DatasetUtils::codeTimeUnit(std::string time_unit_name){
    assert(action == "code");
    std::string line = findLine(TIME_UNIT_KEY, time_unit_name);
    return Conversor::stringToInt(StringUtils::splitByString(line, SEPARATOR)[1]);
}

std::string DatasetUtils::decodeDatasetName(int dataset_int){
    assert(action == "decode");
    std::string line = findLine(DATASET_KEY, Conversor::intToString(dataset_int));
    return StringUtils::splitByString(line, SEPARATOR)[0];
}

std::string DatasetUtils::decodeTimeUnit(int time_unit_int){
    assert(action == "decode");
    std::string line = findLine(TIME_UNIT_KEY, Conversor::intToString(time_unit_int));
    return StringUtils::splitByString(line, SEPARATOR)[0];
}

std::vector<Range*> DatasetUtils::getRangeVector(std::string dataset_name) {
    std::string line = findLine(ALPHABETS_KEY, dataset_name);
    std::string ranges_str = StringUtils::splitByString(line, SEPARATOR)[1]; // "[0,131071],[2500,5000]"
    std::vector<std::string> ranges_str_split = StringUtils::splitByString(ranges_str, "],["); // <"[0,131071", "2500,5000]">
    std::vector<Range*> result;
    for (int i = 0; i < ranges_str_split.size(); i++){
        std::string range_str = StringUtils::removeChars(ranges_str_split[i], "[");
        range_str = StringUtils::removeChars(range_str, "]"); // "2500,5000"
        std::vector<std::string> ranges_vector_str = StringUtils::splitByString(range_str, ","); // <"2500", "5000">
        int min = Conversor::stringToInt(ranges_vector_str[0]); // 2500
        int max = Conversor::stringToInt(ranges_vector_str[1]); // 5000
        result.emplace_back(new Range(min, max));
    }
    return result;
}

void DatasetUtils::close(){
    delete input_file;
}
