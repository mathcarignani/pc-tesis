
#ifndef CPP_PROJECT_DECODER_GAMPS_H
#define CPP_PROJECT_DECODER_GAMPS_H

#include "decoder_base.h"
#include "structs.h"
#include "GAMPSOutput.h"

class DecoderGAMPS: public DecoderBase {

private:
    std::vector<std::vector<std::string>> columns;
    int column_index;

    MappingTable* mapping_table;

    void decodeDataRows() override;

    void decodeTimeDeltaColumn();
    void decodeMappingTable();
    void decodeOtherColumns();
    void decodeNoDataColumns();
    void decodeGAMPSColumns();

    std::vector<std::vector<double>> decodeGAMPSGroup(bool base_signals);
    std::vector<double> decodeGAMPSColumn(bool base_column);

    void decodeWindow(std::vector<double> & column, bool base_column);
    void decodeConstantWindow(std::vector<double> & column, int window_size, bool base_column);

public:
    using DecoderBase::DecoderBase;

};

#endif //CPP_PROJECT_DECODER_GAMPS_H
