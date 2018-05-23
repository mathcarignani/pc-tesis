
#ifndef CPP_PROJECT_CODER_PCA_H
#define CPP_PROJECT_CODER_PCA_H

#include "coder_cols.h"
#include "pca_window.h"

class CoderPCA: public CoderCols {

private:
    void codeColumn() override;
    void codeWindow(PCAWindow & pca_window);

public:
    using CoderCols::CoderCols;
    std::string getInfo() override;
};

#endif //CPP_PROJECT_CODER_PCA_H
