
#ifndef CPP_PROJECT_DATASET_UTILS_H
#define CPP_PROJECT_DATASET_UTILS_H

#include "text_reader.h"

class DatasetUtils {

private:
    const std::string PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/aux";
    const std::string FILENAME = "CONSTANTS"; // "PAPER_CONSTANTS"
    TextReader input_file = TextReader(PATH, FILENAME);
    std::string action;

public:
    DatasetUtils(std::string action_);
    int codeDatasetName(std::string dataset_name);
    std::string decodeDatasetName(int dataset_int);
    int codeTimeUnit(std::string time_unit_name);
    std::string decodeTimeUnit(int time_unit_int);
    void close();

};

#endif //CPP_PROJECT_DATASET_UTILS_H
