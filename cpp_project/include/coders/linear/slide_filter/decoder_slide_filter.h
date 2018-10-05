
#ifndef CPP_PROJECT_DECODER_SLIDE_FILTER_H
#define CPP_PROJECT_DECODER_SLIDE_FILTER_H

#include "decoder_cols.h"

#if MASK_MODE

#include "coder_utils.h"
#include "SlideFiltersEntry.h"
#include "slide_filter_window.h"

class DecoderSlideFilter: public DecoderCols {

private:
    int max_window_size_bit_length;
    Column* column;
    SlideFilterWindow* m_pApproxData;

    std::vector<std::string> decodeDataColumn() override;
    SlideFiltersEntry* decodeEntry();
    SlideFiltersEntry* getAt(std::vector<SlideFiltersEntry*> & m_pCompressData, int position);
    std::vector<DataItem> decompress();

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int max_window_size_);
};

#endif // MASK_MODE

#endif //CPP_PROJECT_DECODER_SLIDE_FILTER_H
