
#include "header_utils.h"

#include "assert.h"
#include "dataset_utils.h"


Dataset HeaderUtils::codeHeader(CSVReader &csv_reader, BitStreamWriter output_file){
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

    // Time Delta|T0N110W|T0N125W|T0N155W|...|T9N140W

    return Dataset();
}

Dataset HeaderUtils::decodeHeader(BitStreamReader input_file, CSVWriter &output_csv){
    std::cout << "DECODING" << std::endl;
    DatasetUtils dataset_utils = DatasetUtils("decode");

    int dataset_int = input_file.getInt(4); // 4 bits for the dataset name
    std::string dataset_name = dataset_utils.decodeDatasetName(dataset_int);
    std::cout << dataset_name << std::endl;

    int time_unit_int = input_file.getInt(4); // 4 bits for the time unit
    std::string time_unit_name = dataset_utils.decodeTimeUnit(time_unit_int);
    std::cout << time_unit_name << std::endl;

    return Dataset();
}
