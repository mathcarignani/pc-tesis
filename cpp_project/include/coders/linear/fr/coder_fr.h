
#ifndef CPP_PROJECT_CODER_FR_H
#define CPP_PROJECT_CODER_FR_H

#include "coder_cols.h"

#if MASK_MODE

#include "fr_window.h"

class CoderFR: public CoderCols {

private:
    int window_size_bit_length;
    std::vector<int> error_thresholds_vector;
    FRWindow* window;

    void codeCoderParams() override;

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

    FRWindow* createWindow();
    void codeWindow();
    void codeItem(DataItem item, int index);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_CODER_FR_H
