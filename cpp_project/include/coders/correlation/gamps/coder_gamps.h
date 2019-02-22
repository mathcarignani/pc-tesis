
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

    MappingTable* mapping_table;
    Mask* nodata_rows_mask;

    void codeCoderParams() override;
    void codeDataRows() override;

    void codeTimeDeltaColumn();
    GAMPSOutput* processOtherColumns();
    void codeMappingTable(GAMPSOutput* gamps_output);
    void codeGAMPSColumns(GAMPSOutput* gamps_output);


    void getNodataRowsMask();
    GAMPSInput* getGAMPSInput();
    CDataStream* getColumn(int column_index);
    GAMPSOutput* getGAMPSOutput(GAMPSInput* gamps_input);

    void codeGAMPSGroup(DynArray<GAMPSEntry>** signals, bool base_signals);
    void codeGAMPSColumn(DynArray<GAMPSEntry>* column, bool base_column);

    void update(DynArray<GAMPSEntry>* column, int & entry_index, GAMPSEntry & current_entry, int & remaining);
    void codeWindow(APCAWindow* window, bool base_column);

public:
    using CoderBase::CoderBase;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

};

#endif //CPP_PROJECT_CODER_GAMPS_H
