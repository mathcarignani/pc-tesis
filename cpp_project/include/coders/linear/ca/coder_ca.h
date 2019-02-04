
#ifndef CPP_PROJECT_CODER_CA_H
#define CPP_PROJECT_CODER_CA_H

#include "coder_cols.h"
#include "ca_window.h"

class CoderCA: public CoderCols {

private:
    std::vector<int> error_thresholds_vector;
    CAWindow* window;

    void codeCoderParams() override;

    void codeColumnBefore() override;
    void codeColumnWhile(int value) override;
    void codeColumnAfter() override;

    CAWindow* createWindow();
    void processValue(int value);

    void codeValueAndCreateNonNanWindow(int value);
    void codeWindow();
    void codeWindow(int window_length, int window_value);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

};

#endif //CPP_PROJECT_CODER_CA_H
