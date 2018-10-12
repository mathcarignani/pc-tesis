
#ifndef CPP_PROJECT_CODER_GAMPS_H
#define CPP_PROJECT_CODER_GAMPS_H

#include "constants.h"
#include "coder_base.h"

class CoderGAMPS: public CoderBase {

private:
    void codeDataRows() override;
    void codeTimeDeltaColumn();
    void codeColumnGroups();
    void codeColumnGroup(int group_index, int total_groups);
    std::vector<int> calculateGroupParams(int group_index, int total_groups, int & base_threshold, int & ratio_threshold);

    int column_index = 0;
    int row_index = 0;
    int delta_sum;
    std::vector<int> time_delta_vector;
    int total_data_rows;

    int max_window_size;
    int max_window_size_bit_length;
    std::vector<int> error_thresholds_vector;

public:
    using CoderBase::CoderBase;
    void setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_);
};

#endif //CPP_PROJECT_CODER_GAMPS_H
