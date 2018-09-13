
#ifndef CPP_PROJECT_CODER_FR_H
#define CPP_PROJECT_CODER_FR_H

#include "coder_cols.h"
#include "fr_window.h"

class CoderFR: public CoderCols {

private:
    int max_window_size;
    int max_window_size_bit_length;
    std::vector<int> error_thresholds_vector;
    FRWindow* window;

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

    void codeWindow();

public:
    using CoderCols::CoderCols;
    void setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_);

};

#endif //CPP_PROJECT_CODER_FR_H
