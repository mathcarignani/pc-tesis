
#ifndef CPP_PROJECT_CODER_CA_H
#define CPP_PROJECT_CODER_CA_H

#include "coder_cols.h"
#include "ca_window.h"

class CoderCA: public CoderCols {

private:
    int window_size;
    std::vector<int> error_thresholds_vector;
    CAWindow window;
    int window_size_bit_length; // same as window.window_size_bit_length

    void codeCoderParams() override;

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

    CAWindow createWindow();
    void codeOriginal(CAWindow & window, std::string x, int x_delta);
    void code(CAWindow & window, std::string x, int x_delta);

    void codeValueAndCreateNonNanWindow(CAWindow & window, std::string x, int x_int);
    void codeWindow(int window_length, std::string window_value);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

};

#endif //CPP_PROJECT_CODER_CA_H
