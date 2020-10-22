
#ifndef CPP_PROJECT_DECODER_SLIDE_FILTER_H
#define CPP_PROJECT_DECODER_SLIDE_FILTER_H

#include "decoder_cols.h"

#if MASK_MODE

#include "SlideFiltersEntry.h"
#include "slide_filter_window.h"
#include "DynArray.h"
#include "DataStream.h"

class DecoderSlideFilter: public DecoderCols {

private:
    Column* column;
    CDataStream* m_pApproxData;
    int current_position;
    SlideFiltersEntry* lastDecodedEntry;

    std::vector<std::string> decodeDataColumn() override;
    int calculateLastDataTimestamp();
    SlideFiltersEntry* decodeEntry();
    SlideFiltersEntry* getAt(int position);
    void addValue(DataItem data_item);
    void addNoData();
    void decompress(std::vector<int> x_coords_vector);

public:
    using DecoderCols::DecoderCols;
};

#endif // MASK_MODE

#endif //CPP_PROJECT_DECODER_SLIDE_FILTER_H
