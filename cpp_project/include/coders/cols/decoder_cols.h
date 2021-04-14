
#ifndef CPP_PROJECT_DECODER_COLS_H
#define CPP_PROJECT_DECODER_COLS_H

#include "decoder_common.h"
#include "column.h"

class DecoderCols: public DecoderCommon {

private:
    void decodeDataRows() override;

    std::vector<std::string> decodeColumn();
    virtual std::vector<std::string> decodeDataColumn() = 0;

protected:
    int column_index;
    Column* column;
#if MASK_MODE
    int first_column_index = 0; // index of the first masked column
#endif // MASK_MODE

public:
    using DecoderCommon::DecoderCommon;

};

#endif //CPP_PROJECT_DECODER_COLS_H
