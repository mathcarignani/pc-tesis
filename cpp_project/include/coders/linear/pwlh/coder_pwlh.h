
#ifndef CPP_PROJECT_CODER_PWLH_H
#define CPP_PROJECT_CODER_PWLH_H

#include "coder_cols.h"
#include "pwlh_window.h"

class CoderPWLH: public CoderCols {

private:
    int window_size;
    std::vector<int> error_thresholds_vector;
    bool integer_mode;
    PWLHWindow* window;

    void codeCoderParams() override;

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

    PWLHWindow* createWindow();
    void codeWindow(PWLHWindow* window);
    void codeWindowDouble(PWLHWindow* window);
    void codeWindowInt(PWLHWindow* window);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_, bool integer_mode_);
};

#endif //CPP_PROJECT_CODER_PWLH_H
