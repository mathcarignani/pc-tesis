
#ifndef CPP_PROJECT_DECODER_COLS_H
#define CPP_PROJECT_DECODER_COLS_H

#include "decoder_base.h"
#include "column.h"

class DecoderCols: public DecoderBase {

private:
    void decodeDataRows() override;

    std::vector<std::string> decodeColumn();
    virtual std::vector<std::string> decodeDataColumn() = 0;

protected:
    int column_index;
    Column* column;

public:
    using DecoderBase::DecoderBase;

};

#endif //CPP_PROJECT_DECODER_COLS_H
