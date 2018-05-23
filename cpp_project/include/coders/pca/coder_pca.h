
#ifndef CPP_PROJECT_CODER_PCA_H
#define CPP_PROJECT_CODER_PCA_H

#include "coder_cols.h"
#include "pca_window.h"

class CoderPCA: public CoderCols {

private:
    int fixed_window_size;
    std::vector<int> error_thresholds_vector;

    void codeColumn() override;
    PCAWindow createWindow();
    void codeWindow(PCAWindow & window);
    void codeWindowAsConstant(PCAWindow & window);
    void codeWindowEachValue(PCAWindow & window);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int fixed_window_size_, std::vector<int> error_thresholds_vector_);
    std::string getInfo() override;
};

#endif //CPP_PROJECT_CODER_PCA_H
