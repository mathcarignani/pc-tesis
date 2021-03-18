
#ifndef CPP_PROJECT_DECODER_CA_H
#define CPP_PROJECT_DECODER_CA_H

#include "decoder_cols.h"

class DecoderCA: public DecoderCols {

private:
    std::string archived_value;
    bool decode_archived_value;

    std::vector<std::string> decodeDataColumn() override;
    void decode(int nodata_sum, int current_time_delta);
    void decodeArchivedValue();
    void decodeWindow(int nodata_sum);
#if MASK_MODE
    void decodeValues(int window_size, std::string value, int nodata_sum);
#else
    void decodeValues(int window_size, std::string value);
#endif

public:
    using DecoderCols::DecoderCols;
};

#endif //CPP_PROJECT_DECODER_CA_H
