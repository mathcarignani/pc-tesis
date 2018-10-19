
#ifndef CPP_PROJECT_DECODER_SLIDE_FILTER_H
#define CPP_PROJECT_DECODER_SLIDE_FILTER_H

#include "decoder_cols.h"

#if MASK_MODE

#include "SlideFiltersEntry.h"
#include "slide_filter_window.h"

class DecoderSlideFilter: public DecoderCols {

private:
    int window_size_bit_length;
    Column* column;
    SlideFilterWindow* m_pApproxData;

//    int current_window_size;
//    std::string current_value;

    std::vector<std::string> decodeDataColumn() override;
    SlideFiltersEntry* decodeEntry();
    SlideFiltersEntry* getAt(std::vector<SlideFiltersEntry*> & m_pCompressData, int position);
    std::vector<DataItem> decompress();

//    void decodeWindow(std::vector<std::string> & column);
//    void createWindow(std::vector<std::string> & column, std::string previous_value);

public:
    using DecoderCols::DecoderCols;
    void setCoderParams(int window_size_);
};

#endif // MASK_MODE

#endif //CPP_PROJECT_DECODER_SLIDE_FILTER_H
