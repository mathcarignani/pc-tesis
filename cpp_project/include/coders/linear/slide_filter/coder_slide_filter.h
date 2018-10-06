
#ifndef CPP_PROJECT_CODER_SLIDE_FILTER_H
#define CPP_PROJECT_CODER_SLIDE_FILTER_H

#include "coder_cols.h"

#if MASK_MODE

#include "SlideFiltersEntry.h"

class SlideFilterWindow;

class CoderSlideFilter: public CoderCols {

private:
    int max_window_size;
    int max_window_size_bit_length;
    std::vector<int> error_thresholds_vector;
    std::vector<SlideFiltersEntry*> entries_vector;
    SlideFilterWindow* m_pSFData;
    SlideFilterWindow* m_pSFOutput;


    int m_nBegin_Point;

    Line m_curU;// Upper bound line
    Line m_curL;// Lower bound line
    Line m_curG;// Current segment
    Line m_prevG;// Previous segment

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

    void add(SlideFiltersEntry & recording);
    void codeEntries();
    void codeEntry(SlideFiltersEntry* recording);

    void compress();
    void initializeU_L(double t1, double v1, double t2, double v2, double eps);
    bool updateUandLforConnectedSegment(Line& curU, Line& curL, Line prevG);
    Line getFittestLine_G(int beginPoint, int endPoint, Line curU, Line curL);
    void recording_mechanism(int& position);
    void filtering_mechanism(int position);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_CODER_SLIDE_FILTER_H
