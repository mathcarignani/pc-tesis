
#ifndef CPP_PROJECT_CODER_APCA_H
#define CPP_PROJECT_CODER_APCA_H

#include "coder_cols.h"
#include "apca_window.h"

class CoderAPCA: public CoderCols {

private:
    int max_window_size;
    std::vector<int> error_thresholds_vector;

    void codeColumn() override;
    APCAWindow createWindow();
    void codeWindow(APCAWindow & window);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_);
};

#endif //CPP_PROJECT_CODER_APCA_H
