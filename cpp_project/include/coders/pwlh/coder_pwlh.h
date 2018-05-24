
#ifndef CPP_PROJECT_CODER_PWLH_H
#define CPP_PROJECT_CODER_PWLH_H

#include "coder_cols.h"
#include "pwlh_window.h"

class CoderPWLH: public CoderCols {

private:
    int max_window_size;
    std::vector<int> error_thresholds_vector;

    void codeColumn() override;
    PWLHWindow createWindow();
    void codeWindow(PWLHWindow & window);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_);
    std::string getInfo() override;
};

#endif //CPP_PROJECT_CODER_PWLH_H
