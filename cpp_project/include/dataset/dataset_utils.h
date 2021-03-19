
#ifndef CPP_PROJECT_DATASET_UTILS_H
#define CPP_PROJECT_DATASET_UTILS_H

#include <vector>
#include "text_reader.h"
#include "range.h"
#include "os_utils.h"

class DatasetUtils {

private:
    // TODO: remove
    const std::string PATH = OSUtils::GIT_PATH + "/constants";
    const std::string FILENAME = "CONSTANTS"; // "PAPER_CONSTANTS"
    const std::string SEPARATOR = "=";
    const std::string DATASET_KEY = "#DATASET";
    const std::string TIME_UNIT_KEY = "#TIME_UNIT";
    const std::string ALPHABETS_KEY = "#ALPHABETS";

    TextReader* input_file;
    std::string action;

    std::string findLine(std::string string_group, std::string string_to_find);

public:
    static const std::vector<std::string> DATASET_NAMES;
    static const int MAX_DATA_ROWS_BITS;
    static const std::vector<std::string> UNITS;
    static const std::vector<int> SCALES;

    static bool validDatasetName(std::string dataset_name);
    static bool validDataRowsCount(int data_rows_count);
    static bool validUnit(std::string unit);
    static bool validScale(std::string scale);

    // TODO: remove
    DatasetUtils(std::string action_);

    int codeDatasetName(std::string dataset_name);
    int codeTimeUnit(std::string time_unit_name);

    std::string decodeDatasetName(int dataset_int);
    std::string decodeTimeUnit(int time_unit_int);

    std::vector<Range*> getRangeVector(std::string dataset_name);
    void close();
};

#endif //CPP_PROJECT_DATASET_UTILS_H
