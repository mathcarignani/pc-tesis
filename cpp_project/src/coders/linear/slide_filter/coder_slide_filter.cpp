
#include "coder_slide_filter.h"
#include "assert.h"
#include "string_utils.h"


void CoderSlideFilter::setCoderParams(int max_window_size_, std::vector<int> error_thresholds_vector_){
    max_window_size = max_window_size_;
    error_thresholds_vector = error_thresholds_vector_;
    max_window_size_bit_length = StringUtils::bitLength(max_window_size);
}

void CoderSlideFilter::codeColumnBefore(){
    last_recodring_position = 0;
    m_nBegin_Point = 0;
    int error_threshold = error_thresholds_vector.at(column_index);
    m_pSFData = new SlideFilterWindow(total_data_rows, error_threshold);
}

void CoderSlideFilter::codeColumnWhile(std::string csv_value){
#if MASK_MODE
    if (Constants::isNoData(csv_value)) { return; } // skip no_data
#endif
    int x_delta = time_delta_vector[row_index]; // >= 0
    m_pSFData->addDataItem(x_delta, csv_value);
}

void CoderSlideFilter::codeColumnAfter() {
    std::cout << "window.length = " << m_pSFData->length << std::endl;
    std::cout << "total_data_rows = " << total_data_rows << std::endl;
    assert(m_pSFData->length == total_data_rows);
    compress();
}

void CoderSlideFilter::codeEntry(SlideFiltersEntry recording){
    int connToFollow_int = (recording.connToFollow) ? 1 : 0;

    int recording_position = m_pSFData->getPosition(recording.timestamp);
    int position = recording_position - last_recodring_position; // position = recording_position in the first call

    std::cout << "timestamp= " << recording.timestamp << std::endl;
    std::cout << "recording_position = " << recording_position << std::endl;
    std::cout << connToFollow_int << " " << recording.value << " " << recording_position << std::endl;
    std::cout << connToFollow_int << " " << recording.value << " " << position << std::endl;
    last_recodring_position = recording_position;

    codeBit(connToFollow_int);
    codeFloat(recording.value);
//    assert(position < max_window_size);
//    codeInt(position, max_window_size_bit_length);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// compress raw data
void CoderSlideFilter::compress()
{
    int inputSize = m_pSFData->getDataLength();
    if (inputSize == 1)
    {
        DataItem item = m_pSFData->getAt(0);
        SlideFiltersEntry recording(item.value, item.timestamp, true);
        codeEntry(recording); // m_pSFOutput->getCompressData()->add(recording);
        m_nBegin_Point = 1;
        return;
    }

    // Initialize upper bound and lower bound
    double eps = m_pSFData->getEsp();
    DataItem item1 = m_pSFData->getAt(0);
    DataItem item2 = m_pSFData->getAt(1);
    initializeU_L(item1.timestamp, item1.value, item2.timestamp, item2.value, eps);

    //Read the input
    double upperValue, lowerValue;
    DataItem item;
    for (int i = 2; i <= inputSize; i++)
    {
        //Read if it is not the end of the input
        if (i < inputSize)
        {
            item = m_pSFData->getAt(i);
            upperValue = m_curU.getValue(item.timestamp);
            lowerValue = m_curL.getValue(item.timestamp);
        }

        //recording mechanism
        bool violated_constraint = (item.value - upperValue > eps) || (lowerValue - item.value > eps);
        if ((i == inputSize) || violated_constraint)
        {
            std::cout << "recording_mechanism(i)" << std::endl;
            recording_mechanism(i);
        }
        else //filtering mechanism
        {
            filtering_mechanism(i);
        }
    }
}

// Initialize upper bound and lower bound
void CoderSlideFilter::initializeU_L(double t1, double v1, double t2, double v2, double eps)
{
    Point top1(v1 + eps, t1);
    Point bottom1(v1 - eps, t1);
    Point top2(v2 + eps, t2);
    Point bottom2(v2- eps, t2);
    m_curL.update(&top1, &bottom2);
    m_curU.update(&bottom1, &top2);
}

// Update upper bound and lower bound
bool CoderSlideFilter::updateUandLforConnectedSegment(Line& curU, Line& curL, Line prevG)
{
    if (m_nBegin_Point ==0)
        return false;

    Point ul = curU.getIntersection(&curL);
    DataItem preItem= m_pSFData->getAt(m_nBegin_Point - 1);
    DataItem firstItem = m_pSFData->getAt(m_nBegin_Point);

    // Compute alpha, beta
    Point alpha(prevG.getValue(preItem.timestamp), preItem.timestamp);
    Point beta(prevG.getValue(firstItem.timestamp), firstItem.timestamp);
    Line alpha_ul(&ul,&alpha);
    Line beta_ul(&ul, &beta);

    double minSlope, maxSlope;
    if (alpha_ul.getSlope() < beta_ul.getSlope())
    {
        minSlope = alpha_ul.getSlope();
        maxSlope = beta_ul.getSlope();
    }
    else
    {
        maxSlope = alpha_ul.getSlope();
        minSlope = beta_ul.getSlope();
    }

    // Check whether current segment is connected with previous 'prevG'
    bool isConnected = false;
    if (minSlope < curU.getSlope() && maxSlope > curL.getSlope())
    {
        Point ul = curU.getIntersection(&curL);
        isConnected = true;

        // Update bounds
        if (maxSlope < curU.getSlope())
        {
            curU.update(&ul,maxSlope);
        }
        if (minSlope > curL.getSlope())
        {
            curL.update(&ul,minSlope);
        }
    }

    return isConnected;
}

// Find the fittest line in range of lower bound and upper bound
Line CoderSlideFilter::getFittestLine_G(int beginPoint, int endPoint, Line curU, Line curL)
{
    Point ul = curU.getIntersection(curL);
    double numberator = 0;
    double denominator = 0;

    for (int j = beginPoint + 1; j < endPoint;  j++)
    {
        DataItem item = m_pSFData->getAt(j);
        numberator += (item.value - ul.y) * (item.timestamp - ul.x);
        denominator += (item.timestamp - ul.x) * (item.timestamp - ul.x);
    }

    double fraction = numberator / denominator;
    double slopeU = curU.getSlope();
    double slopeL = curL.getSlope();

    // Get fittest slope in range of lower and upper bounds
    double fittestSlope = fraction > slopeU ? slopeU : fraction;
    fittestSlope = fittestSlope > slopeL ? fittestSlope : slopeL;

    // Create fittest line
    Line fittestLine;
    fittestLine.setSlope(fittestSlope);
    fittestLine.setIntercept(ul.y - (fittestSlope * ul.x));
    return fittestLine;
}

// Generate line segments for the filtering intervals and update the latest-executed point
void CoderSlideFilter::recording_mechanism(int& position)
{
    int inputSize = m_pSFData->getDataLength();
    bool existInter;
    DataItem begin_curSeg = m_pSFData->getAt(m_nBegin_Point);

    existInter = updateUandLforConnectedSegment(m_curU,m_curL,m_prevG);
    m_curG = getFittestLine_G(m_nBegin_Point, position, m_curU, m_curL);

    if (m_nBegin_Point == 0)
    {
        std::cout << "1" << std::endl;
        //Create first recording
        double t = begin_curSeg.timestamp;
        SlideFiltersEntry sfe(m_curG.getValue(t), t , true); // SlideFiltersEntry* sfe = &SlideFiltersEntry(m_curG.getValue(t), t , true);
        //m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t , true));
        codeEntry(sfe); // m_pSFOutput->getCompressData()->add(*sfe);
    }
    else if (existInter)
    {
        std::cout << "2" << std::endl;
        //m_curG cut m_prevG at valid section
        Point inter = m_curG.getIntersection(m_prevG);
        SlideFiltersEntry recording(inter, existInter);
        codeEntry(recording); // m_pSFOutput->getCompressData()->add(recording);
    }
    else
    {
        std::cout << "3" << std::endl;
        //m_curG cut m_prevG at invalid section
        DataItem end_prevSeg = m_pSFData->getAt(m_nBegin_Point - 1);
        double t = end_prevSeg.timestamp;
        SlideFiltersEntry sfe(m_prevG.getValue(t), t, existInter); // SlideFiltersEntry* sfe = &SlideFiltersEntry(m_prevG.getValue(t), t, existInter);
        //m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_prevG.getValue(t), t, existInter));
        codeEntry(sfe); // m_pSFOutput->getCompressData()->add(*sfe);
        t = begin_curSeg.timestamp;
        SlideFiltersEntry sfe2(m_curG.getValue(t), t, true); // sfe = &SlideFiltersEntry(m_curG.getValue(t), t, true);
        //m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t, true));
        codeEntry(sfe2); // m_pSFOutput->getCompressData()->add(*sfe);
    }

    if (position < inputSize -1)
    {
        std::cout << "4" << std::endl;
        //Create new interval by two points
        m_nBegin_Point = position;
        DataItem curItem = m_pSFData->getAt(position);
        position++;
        DataItem nextItem = m_pSFData->getAt(position);
        double eps = m_pSFData->getEsp();
        initializeU_L(curItem.timestamp, curItem.value, nextItem.timestamp, nextItem.value, eps);
        m_prevG = m_curG;
    }
        //if last interval has only one point --> Create last recording and finish compressing
    else if (position == (inputSize - 1))
    {
        std::cout << "5" << std::endl;
        m_nBegin_Point = position;
        DataItem preItem = m_pSFData->getAt(m_nBegin_Point - 1);
        DataItem item = m_pSFData->getAt(position);
        double t = preItem.timestamp;
        SlideFiltersEntry(m_curG.getValue(t), t, true);
        SlideFiltersEntry sfe(m_curG.getValue(t), t, true); // SlideFiltersEntry* sfe = &SlideFiltersEntry(m_curG.getValue(t), t, true);
        //m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t, true));
        codeEntry(sfe); // m_pSFOutput->getCompressData()->add(*sfe);
        SlideFiltersEntry sfe2(item.value, item.timestamp, false); // sfe = &SlideFiltersEntry(item.value, item.timestamp, false);
        //m_pSFOutput->getCompressData()->add(SlideFiltersEntry(item.value, item.timestamp, false));
        codeEntry(sfe2); // m_pSFOutput->getCompressData()->add(*sfe);
        position++;
    }
        //position == inputSize --> Create last recording
    else
    {
        std::cout << "6" << std::endl;
        DataItem item = m_pSFData->getAt(position - 1);
        double t = item.timestamp;
        SlideFiltersEntry sfe(m_curG.getValue(t), t, false); // SlideFiltersEntry* sfe = &SlideFiltersEntry(m_curG.getValue(t), t, false);
        //m_pSFOutput->getCompressData()->add(SlideFiltersEntry(m_curG.getValue(t), t, false));
        codeEntry(sfe); // m_pSFOutput->getCompressData()->add(*sfe);
    }
}

// Adjust upper bound and lower bound with the arrival of each new data point at 'position'
void CoderSlideFilter::filtering_mechanism(int position)
{
    DataItem item = m_pSFData->getAt(position);
    double upperValue = m_curU.getValue(item.timestamp);
    double lowerValue = m_curL.getValue(item.timestamp);
    int j;

    double eps = m_pSFData->getEsp();
    Point top(item.value + eps, item.timestamp);
    Point bottom(item.value - eps, item.timestamp);
    DataItem tmpItem;

    //item is above L a distance which is larger than epsilon
    if (item.value - lowerValue > eps)
    {
        //Update L
        for (j = m_nBegin_Point; j < position; j++)
        {
            tmpItem = m_pSFData->getAt(j);
            Point tmpTop(tmpItem.value + eps, tmpItem.timestamp);
            Line tmpL(&tmpTop, &bottom);

            if (tmpL.getSlope() > m_curL.getSlope())
            {
                m_curL.setSlope(tmpL.getSlope());
                m_curL.setIntercept(tmpL.getIntercept());
            }
        }
    }

    //item is under U a distance which is larger than epsilon
    if (upperValue - item.value > eps)
    {
        //Update U
        for (j = m_nBegin_Point; j < position; j++)
        {
            tmpItem = m_pSFData->getAt(j);
            Point tmpBottom(tmpItem.value - eps, tmpItem.timestamp);
            Line tmpU(&tmpBottom, &top);

            if (tmpU.getSlope() < m_curU.getSlope())
            {
                m_curU.setSlope(tmpU.getSlope());
                m_curU.setIntercept(tmpU.getIntercept());
            }
        }
    }
}
