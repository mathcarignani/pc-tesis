
#ifndef CPP_PROJECT_CODER_SLIDE_FILTER_H
#define CPP_PROJECT_CODER_SLIDE_FILTER_H

#include "coder_cols.h"

#if MASK_MODE

#include "SlideFiltersEntry.h"

class SlideFilterWindow;

class CoderSlideFilter: public CoderCols {

private:
    std::vector<int> error_thresholds_vector;
    SlideFilterWindow* data;
    SlideFilterWindow* m_pSFData;

    int m_nBegin_Point;

    Line m_curU;// Upper bound line
    Line m_curL;// Lower bound line
    Line m_curG;// Current segment
    Line m_prevG;// Previous segment

    void codeCoderParams() override;

    void codeColumnBefore() override;
    void codeColumnWhile(std::string csv_value) override;
    void codeColumnAfter() override;

    void codeEntry(bool connToFollow, float timestamp, float value);

    void compress();
    void compressWindow();
    void initializeU_L(float t1, float v1, float t2, float v2, float eps);
    bool updateUandLforConnectedSegment(Line& curU, Line& curL, Line prevG);
    Line getFittestLine_G(int beginPoint, int endPoint, Line curU, Line curL);
    void recording_mechanism(int& position);
    void filtering_mechanism(int position);

public:
    using CoderCols::CoderCols;
    void setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_);

};

#endif // MASK_MODE

#endif //CPP_PROJECT_CODER_SLIDE_FILTER_H
