
#include "time_delta_coder.h"
#include "conversor.h"
#include "coder_utils.h"
#include "apca_window.h"

std::vector<int> TimeDeltaCoder::code(CoderCommon* coder){
    // CoderAPCA::codeColumnBefore begin
    int window_size = 256; // TODO: change window_size depending on the dataset
    int error_threshold = 0;
    bool mask_mode = false;
    APCAWindow* window = new APCAWindow(window_size, error_threshold, mask_mode);
    // CoderAPCA::codeColumnBefore end

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
        // add int value to the time_delta_vector
        int csv_value_int = Conversor::stringToInt(csv_value);
        time_delta_vector.push_back(csv_value_int);

        // CoderAPCA::codeColumnWhile begin
        if (!window->conditionHolds(csv_value)){
            // CoderAPCA::codeWindow begin
            coder->codeWindowLength((Window*) window);
            coder->codeValueRaw(window->constant_value);
            // CoderAPCA::codeWindow end
            window->addFirstValue(csv_value);
        }
        // CoderAPCA::codeColumnWhile end
    }
    // CoderAPCA::codeColumnAfter begin
    if (!window->isEmpty()){
        // CoderAPCA::codeWindow begin
        coder->codeWindowLength((Window*) window);
        coder->codeValueRaw(window->constant_value);
        // CoderAPCA::codeWindow end
    }
    // CoderAPCA::codeColumnAfter begin
    return time_delta_vector;
}
