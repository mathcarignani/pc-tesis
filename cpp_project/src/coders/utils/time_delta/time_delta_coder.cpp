
#include "time_delta_coder.h"
#include "string_utils.h"
#include "coder_utils.h"

//
// TODO: use a more appropriate lossless compression schema for coding the time delta column.
//
std::vector<int> TimeDeltaCoder::code(CoderBase* coder){
    CSVReader* input_csv = coder->input_csv;

    std::vector<int> time_delta_vector{};
    input_csv->goToFirstDataRow(0);
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        std::string mapped_value = CoderUtils::mapValue(csv_value, 0);
        coder->codeValueRaw(mapped_value); // same as CoderBasic

        // add int value to the time_delta_vector
        int csv_value_int = StringUtils::stringToInt(csv_value);
        time_delta_vector.push_back(csv_value_int);
    }
    return time_delta_vector;
}
