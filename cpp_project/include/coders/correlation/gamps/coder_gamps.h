
#ifndef CPP_PROJECT_CODER_GAMPS_H
#define CPP_PROJECT_CODER_GAMPS_H

#include "coder_base.h"
#include "apca_window.h"

class CoderGAMPS: public CoderBase {

private:
    std::vector<int> error_thresholds_vector;

    int column_index;
    int row_index;
    int delta_sum;
    std::vector<int> time_delta_vector;
    int total_data_rows;
    APCAWindow* window;

    void codeCoderParams() override;

    void codeDataRows() override;
    void codeTimeDeltaColumn();
    void codeColumnGroups();
    void codeColumnGroup(int group_index);

    // TODO: merge these two methods into one
    std::vector<int> codeBaseColumn(int error_threshold);
    void codeRatioColumn(int error_threshold, std::vector<int> base_column);

    void groupThresholds(int threshold, int & base_threshold, int & ratio_threshold);


    static int calculateDiff(int base_value, int ratio_value);

public:
    using CoderBase::CoderBase;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

};

#endif //CPP_PROJECT_CODER_GAMPS_H
