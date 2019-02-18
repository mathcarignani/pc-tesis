
#ifndef CPP_PROJECT_CODER_GAMPS_H
#define CPP_PROJECT_CODER_GAMPS_H

#include "coder_base.h"
#include "apca_window.h"
#include "structs.h"

#include "DataStream.h"
#include "GAMPSOutput.h"
#include "mask.h"

class CoderGAMPS: public CoderBase {

private:
    std::vector<int> error_thresholds_vector;

    int column_index;
    int row_index;
    std::vector<int> time_delta_vector;
    int total_data_rows;
    APCAWindow* window;

    MappingTable* mapping_table;

    void codeCoderParams() override;

    void codeDataRows() override;
    void codeTimeDeltaColumn();
    Mask* getNodataRowsMask();
    GAMPSInput* getGAMPSInput(Mask* nodata_rows_mask);
    GAMPSOutput* getGAMPSOutput(GAMPSInput* gamps_input);

    void codeMappingTable(GAMPSOutput* gamps_output);
    void codeColumnGroups(GAMPSOutput* gamps_output);
    void codeColumn(DynArray<GAMPSEntry>* temp);

    CDataStream* getColumn(int column_index, Mask* nodata_rows_mask);

public:
    using CoderBase::CoderBase;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

};

#endif //CPP_PROJECT_CODER_GAMPS_H
