
#ifndef CPP_PROJECT_CODER_GAMPS_H
#define CPP_PROJECT_CODER_GAMPS_H

#include "coder_common.h"
#include "apca_window.h"
#include "mapping_table.h"

#include "DataStream.h"
#include "GAMPSOutput.h"
#include "GAMPS.h"
#include "mask.h"

class CoderGAMPS: public CoderCommon {

private:
    std::vector<int> error_thresholds_vector;
    bool limit_mode;

    int total_groups;
    int group_index;
    int total_group_columns; // total number of columns in a group (same for every group)

    int column_index;
    int row_index;
    std::vector<int> time_delta_vector;

    std::vector<double> gamps_epsilons_vector;
    GAMPSInput* gamps_input;
    GAMPS* gamps;

    MappingTable* mapping_table;
    Mask* nodata_rows_mask;

#if MASK_MODE == 3
    std::vector<int> total_data_rows_vector;
#endif // MASK_MODE == 3

    void codeCoderParams() override;
    void codeDataRows() override;

    void codeTimeDeltaColumn();
    void codeGroup();
    GAMPSOutput* processOtherColumns();
    void codeMappingTable(GAMPSOutput* gamps_output);
    void codeGAMPSColumns(GAMPSOutput* gamps_output);


    void getNodataRowsMask();
    GAMPSInput* getGAMPSInput();
    CDataStream* getColumn(int column_index);
    GAMPSOutput* getGAMPSOutput();

    void codeGAMPSColumn(DynArray<GAMPSEntry>* column);

    void update(DynArray<GAMPSEntry>* column, int & entry_index, GAMPSEntry & current_entry, int & remaining);
    void codeWindow(APCAWindow* window);

public:
    using CoderCommon::CoderCommon;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_, bool limit_mode_);

};

#endif //CPP_PROJECT_CODER_GAMPS_H
