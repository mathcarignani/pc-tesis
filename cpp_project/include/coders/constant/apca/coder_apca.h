
#ifndef CPP_PROJECT_CODER_APCA_H
#define CPP_PROJECT_CODER_APCA_H

#include "coder_cols.h"
#include "apca_window.h"

class CoderAPCA: public CoderCols {

private:
    std::vector<int> error_thresholds_vector;
    APCAWindow* window;

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

public:
    using CoderCols::CoderCols;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);
    void codeWindow(APCAWindow* window);
};

#endif //CPP_PROJECT_CODER_APCA_H
