
#ifndef CPP_PROJECT_CODER_SLIDE_FILTER_H
#define CPP_PROJECT_CODER_SLIDE_FILTER_H

#include "coder_cols.h"
#include "slide_filter_window.h"

class CoderSlideFilter: public CoderCols {

private:
    int max_window_size;
    std::vector<int> error_thresholds_vector;

    void codeColumn() override;
    SlideFilterWindow createWindow();
    void codeWindow(SlideFilterWindow & window);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_);
    std::string getInfo() override;
};

#endif //CPP_PROJECT_CODER_SLIDE_FILTER_H
