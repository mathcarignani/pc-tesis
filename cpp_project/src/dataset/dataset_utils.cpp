
#include "dataset_utils.h"

#include "assert.h"

DatasetUtils::DatasetUtils(std::string action_){
    assert(action_ == "code" || action_ == "decode");
    action = action_;
}

int DatasetUtils::codeDatasetName(std::string dataset_name){

}

std::string DatasetUtils::decodeDatasetName(int dataset_int){

}

int DatasetUtils::codeTimeUnit(std::string time_unit_name){

}

std::string DatasetUtils::decodeTimeUnit(int time_unit_int){

}

void DatasetUtils::close(){
    input_file.close();
}
