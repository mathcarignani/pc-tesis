
#ifndef CPP_PROJECT_MASK_CODER_H
#define CPP_PROJECT_MASK_CODER_H

#include "constants.h"

#if MASK_MODE

#include "dataset.h"
#include "csv_reader.h"
#include "coder_base.h"

class MaskCoder {

public:
    static int code(CoderBase* coder, Dataset* dataset, CSVReader* input_csv, int column_index);

private:
    static int codeBurst(CoderBase* coder, bool burst_is_no_data, int burst_length);
};

#endif // MASK_MODE

#endif //CPP_PROJECT_MASK_CODER_H
