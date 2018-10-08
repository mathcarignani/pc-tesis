
#include "coder_fr.h"

#if MASK_MODE

#include "math_utils.h"
#include "string_utils.h"
#include "assert.h"

void CoderFR::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    max_window_size_bit_length = MathUtils::bitLength(max_window_size);
}

void CoderFR::codeColumnBefore(){
    delta_sum = 0;
    window = createWindow();
}

void CoderFR::codeColumnWhile(std::string csv_value) {
    delta_sum += time_delta_vector[row_index]; // >= 0
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
    window->addDataItem(delta_sum, csv_value);
    if (window->isFull()){
        codeWindow();
        window->clear();
    }
    delta_sum = 0;
}

void CoderFR::codeColumnAfter() {
    if (window->isEmpty()) { return; }
    assert(!window->isFull());
    codeWindow();
}

FRWindow* CoderFR::createWindow(){
    int error_threshold = error_thresholds_vector.at(column_index);
    return new FRWindow(max_window_size, error_threshold);
}

void CoderFR::codeWindow(){
    std::vector<DataItem> items = window->getItems();

    int size = items.size(); // 1 <= size <= max_window_size
    assert(size <= max_window_size);
    for(int i=0; i < size; i++){
        DataItem item = items[i];
        codeItem(item, i);
    }
}

void CoderFR::codeItem(DataItem item, int index){
    int value = (int) item.value;
    std::string value_str = StringUtils::intToString(value);
    codeValueRaw(value_str);
    // we always code the value in the first index, so we don't have to code its index
    if (index == 0) { return; }
    codeInt(item.timestamp, max_window_size_bit_length); // 1 <= index <= max_window_size
}

#endif // MASK_MODE
