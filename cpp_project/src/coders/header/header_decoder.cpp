
#include "header_decoder.h"

#include "assert.h"
#include "string_utils.h"
#include "dataset_utils.h"


Dataset HeaderDecoder::decodeHeader(){
    std::cout << "DECODING..." << std::endl;
    DatasetUtils dataset_utils = DatasetUtils("decode");
    decodeDatasetName(dataset_utils);
    decodeTimeUnit(dataset_utils);
    decodeFirstTimestamp();
    decodeColumnNames();
    return Dataset();
}

void HeaderDecoder::decodeDatasetName(DatasetUtils & dataset_utils){
    int dataset_int = input_file.getInt(4); // 4 bits for the dataset name
    std::string dataset_name = dataset_utils.decodeDatasetName(dataset_int);
    std::vector<std::string> row = {"DATASET:", dataset_name};
    output_csv.writeRow(row);
}

void HeaderDecoder::decodeTimeUnit(DatasetUtils & dataset_utils){
    int time_unit_int = input_file.getInt(4); // 4 bits for the time unit
    std::string time_unit_name = dataset_utils.decodeTimeUnit(time_unit_int);
}
void HeaderDecoder::decodeFirstTimestamp(){
    long int seconds = input_file.getInt(32); // 32 bits for the timestamp
    std::cout << seconds;
//    std::string time_unit_name = dataset_utils.decodeTimeUnit(time_unit_int);
}

std::string HeaderDecoder::decodeTimestamp(long int seconds){
//    assert(action == "decode");


}

void HeaderDecoder::decodeColumnNames(){

}