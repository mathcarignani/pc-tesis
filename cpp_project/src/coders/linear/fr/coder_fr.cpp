
#include "coder_fr.h"
#include "math_utils.h"
#include "string_utils.h"
#include "assert.h"

void CoderFR::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    max_window_size_bit_length = MathUtils::bitLength(max_window_size);
}

void CoderFR::codeColumnBefore(){
    int error_threshold = error_thresholds_vector.at(column_index);
    window = new FRWindow(max_window_size, error_threshold);
}

void CoderFR::codeColumnWhile(std::string csv_value) {
#if MASK_MODE
    // TODO: consider x_delta
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
#endif
    int x_delta = time_delta_vector[row_index]; // >= 0
    window->addDataItem(x_delta, csv_value);
    if (window->isFull()){
        codeWindow();
        window->clear();
    }
}

void CoderFR::codeColumnAfter() {
    if (window->isEmpty()) { return; }
    assert(!window->isFull());
}

void CoderFR::codeWindow(){
    std::vector<DataItem> items = window->getItems();

    int size = items.size();
    assert(size <= max_window_size);
    for(int i=0; i < size; i++){
        DataItem item = items[i];
        int value = (int) item.value;
        codeValueRaw(StringUtils::intToString(value));
        if (i != 0){
            codeInt(i, max_window_size_bit_length);
        }
    }
}