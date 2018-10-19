
#ifndef CPP_PROJECT_DECODER_GAMPS_H
#define CPP_PROJECT_DECODER_GAMPS_H

#include "decoder_base.h"

class DecoderGAMPS: public DecoderBase {

private:
    std::vector<std::vector<std::string>> columns;
    int column_index;

    void decodeDataRows() override;
    void decodeTimeDeltaColumn();
    void decodeColumnGroups();
    void decodeColumnGroup(int group_index);
    std::vector<std::string> decodeBaseColumn();
    void decodeRatioColumn(std::vector<std::string> base_column);
    static std::string calculateRatio(std::string base_value, std::string diff_value);

public:
    using DecoderBase::DecoderBase;
    void setCoderParams(int window_size_);

};

#endif //CPP_PROJECT_DECODER_GAMPS_H
