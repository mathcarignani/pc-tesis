
#ifndef CPP_PROJECT_CODER_GAMPS_H
#define CPP_PROJECT_CODER_GAMPS_H

#include "coder_common.h"
#include "apca_window.h"
#include "mapping_table.h"

#include "GAMPSOutput.h"
#include "mask.h"

class CoderGAMPS: public CoderCommon {

private:
    bool limit_mode;
    int column_index;
    int row_index;
    std::vector<int> time_delta_vector;
    Mask* nodata_rows_mask;

#if MASK_MODE == 3
    std::vector<int> total_data_rows_vector;
#endif // MASK_MODE == 3

    void codeCoderParams() override;
    void codeDataRows() override;

    void codeTimeDeltaColumn();
    void codeDataTypeColumns();

    void codeMappingTable(GAMPSOutput* gamps_output);
    void codeGAMPSColumns(GAMPSOutput* gamps_output);

    void codeGAMPSColumn(DynArray<GAMPSEntry>* column, bool base_window);

    void update(DynArray<GAMPSEntry>* column, int & entry_index, GAMPSEntry & current_entry, int & remaining);
    void codeWindow(APCAWindow* window, bool base_window);

public:
    // These attributes are public because they are accessed by the GroupGAMPS class
    std::vector<int> error_thresholds_vector;
    int total_data_types;
    int data_type_index;
    int total_data_type_columns; // total number of columns for each data type (they are the same for every data type)
    MappingTable* mapping_table;

    using CoderCommon::CoderCommon;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_, bool limit_mode_);

};

#endif //CPP_PROJECT_CODER_GAMPS_H
