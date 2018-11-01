
#ifndef CPP_PROJECT_CODER_APCA_H
#define CPP_PROJECT_CODER_APCA_H

#include "coder_cols.h"
#include "apca_window.h"

class CoderAPCA: public CoderCols {

private:
    int window_size;
    std::vector<int> error_thresholds_vector;
    APCAWindow* window;

    void codeCoderParams() override;

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

public:
    using CoderCols::CoderCols;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

    //
    // Wrapper methods which are also used by CoderGAMPS.
    //
    static void codeColumnWhile(CoderBase* coder, APCAWindow* window, std::string csv_value);
    static void codeColumnAfter(CoderBase* coder, APCAWindow* window);
    static void codeWindow(CoderBase* coder, APCAWindow* window);
};

#endif //CPP_PROJECT_CODER_APCA_H
