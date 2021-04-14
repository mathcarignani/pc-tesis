
#include "time_delta_coder.h"
#include "conversor.h"
#include "coder_utils.h"

//
// TODO: use a more appropriate lossless compression schema for coding the time delta column.
//
std::vector<int> TimeDeltaCoder::code(CoderCommon* coder){
    CSVReader* input_csv = coder->input_csv;

    std::vector<int> time_delta_vector{};
    input_csv->goToFirstDataRow(0);
    bool first_value = true;
    while (input_csv->continue_reading){
        std::string csv_value = input_csv->readNextValue();
        if (first_value){
            assert(csv_value == "0");
            first_value = false;
        }
        coder->codeValueRaw(csv_value); // same as CoderBase

        // add int value to the time_delta_vector
        int csv_value_int = Conversor::stringToInt(csv_value);
        time_delta_vector.push_back(csv_value_int);
    }
    return time_delta_vector;
}
