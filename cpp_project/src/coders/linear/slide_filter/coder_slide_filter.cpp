
#include "coder_slide_filter.h"
#include "slide_filter_window.h"

#if MASK_MODE

#include "assert.h"
#include "math_utils.h"
#include <iomanip>
#include "coder_utils.h"

void CoderSlideFilter::setCoderParams(int window_size_, std::vector<int> error_thresholds_vector_){
    window_size = window_size_;
    error_thresholds_vector = error_thresholds_vector_;
}

void CoderSlideFilter::codeCoderParams(){
    codeCoderParameters(Constants::CODER_SF, window_size);
}

void CoderSlideFilter::codeColumnBefore(){
    delta_sum = 0;
    int error_threshold = error_thresholds_vector.at(column_index);
    data = new SlideFilterWindow(total_data_rows, error_threshold);
}

void CoderSlideFilter::codeColumnWhile(std::string csv_value){
    int delta = time_delta_vector[row_index]; // >= 0
    if (Constants::isNoData(csv_value)) {
        delta_sum += delta; // delta >= 0
        return; // skip no_data
    }
    delta_sum += CoderUtils::calculateDelta(delta, row_index);
//    std::cout << "I=" << row_index << "----- " << delta_sum << " ------------------------> " << csv_value << std::endl;
    data->addDataItem(delta_sum, csv_value);
    delta_sum = 0;
}

void CoderSlideFilter::codeColumnAfter() {
    assert(data->length == total_data_rows);
    if (total_data_rows > 0){
        compress();
    }
    delete data;
}

void CoderSlideFilter::codeEntry(bool connToFollow, float timestamp, float value){
    if (column_index == 1){
        std::cout.precision(17);
        std::cout << "----- " << connToFollow << " " << (float) timestamp << " " << (float) value << std::endl;
    }
    codeBool(connToFollow);
    codeFloat(timestamp);
    codeFloat(value);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void CoderSlideFilter::compress(){
    int inputSize = data->getDataLength();
    int i = 0;

//    std::cout << "inputSize = " << inputSize << std::endl;
//    std::cout << "window_size = " << window_size << std::endl;
    int error_threshold = error_thresholds_vector.at(column_index);

    while(i < inputSize) {
        int win_size = ((inputSize - i) < window_size) ? (inputSize - i) : window_size;
//        std::cout << "win_size = " << win_size << std::endl;

        m_pSFData = new SlideFilterWindow(win_size, error_threshold);
        int first_timestamp = data->getAt(i).timestamp;
        for(int j = i; j < i + win_size; j++){
            DataItem item2 = data->getAt(j);
            int diff_timestamp = item2.timestamp - first_timestamp; // the first timestamp is always 0
            m_pSFData->addDataItemTwo(diff_timestamp, item2.value);
//            std::cout << "  i=" << i << "  => (" << diff_timestamp << ", " << item2.value << ")" <<  std::endl;
        }
        compressWindow();
        delete m_pSFData;
        i += win_size;
    }
//    m_pSFData = data;
//    compressWindow();
}


// compress raw data
void CoderSlideFilter::compressWindow()
{
    m_nBegin_Point = 0;
//    std::cout << "compressWindow()" << std::endl;
    int inputSize = m_pSFData->getDataLength();
    if (inputSize == 1)
    {
        DataItem item = m_pSFData->getAt(0);
        codeEntry(true, item.timestamp, item.value);
        m_nBegin_Point = 1;
        return;
    }

    // Initialize upper bound and lower bound
//    double eps = m_pSFData->getEsp();
    float eps = m_pSFData->getEsp();
    DataItem item1 = m_pSFData->getAt(0);
    DataItem item2 = m_pSFData->getAt(1);
    initializeU_L(item1.timestamp, item1.value, item2.timestamp, item2.value, eps);

    //Read the input
//    double upperValue, lowerValue;
    float upperValue, lowerValue;
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
        if ((i == inputSize) || (item.value - upperValue > eps) || (lowerValue - item.value > eps))
        {
            recording_mechanism(i);
        }
        else //filtering mechanism
        {
            filtering_mechanism(i);
        }
    }
//    item = m_pSFData->getAt(inputSize - 1);
//    std::cout << "item.timestamp = " << item.timestamp << std::endl;
}

// Initialize upper bound and lower bound
//void CoderSlideFilter::initializeU_L(double t1, double v1, double t2, double v2, double eps)
void CoderSlideFilter::initializeU_L(float t1, float v1, float t2, float v2, float eps)
{
    if (column_index == 1){
        std::cout << "CoderSlideFilter::initializeU_L((" << t1 << ", " << v1 << "), (" << t2 << ", " << v2 << "), " << eps << ")" << std::endl;
    }
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
    if (column_index == 1){
        std::cout << "CoderSlideFilter::updateUandLforConnectedSegment(...)" << std::endl;
        std::cout << "    curU: ";
        curU.print();
        std::cout << "    curL: ";
        curL.print();
        std::cout << "    prevG: ";
        prevG.print();
    }
    if (m_nBegin_Point ==0)
        return false;

    Point ul = curU.getIntersection(&curL);
    if (column_index == 1){
        ul.print();
    }
    DataItem preItem= m_pSFData->getAt(m_nBegin_Point - 1);
    DataItem firstItem = m_pSFData->getAt(m_nBegin_Point);

    // Compute alpha, beta
    Point alpha(prevG.getValue(preItem.timestamp), preItem.timestamp);
    Point beta(prevG.getValue(firstItem.timestamp), firstItem.timestamp);
    Line alpha_ul(&ul,&alpha);
    Line beta_ul(&ul, &beta);
    if (column_index == 1){
        alpha.print();
        beta.print();
        alpha_ul.print();
        beta_ul.print();
    }

//    double minSlope, maxSlope;
    float minSlope, maxSlope;
    if (alpha_ul.getSlope() < beta_ul.getSlope())
    {
        if (column_index == 1){
            std::cout << "    alpha_ul.getSlope() < beta_ul.getSlope()" << std::endl;
        }
        minSlope = alpha_ul.getSlope();
        maxSlope = beta_ul.getSlope();
    }
    else
    {
        if (column_index == 1){
            std::cout << "    ELSE alpha_ul.getSlope() < beta_ul.getSlope()" << std::endl;
        }
        maxSlope = alpha_ul.getSlope();
        minSlope = beta_ul.getSlope();
    }

    // Check whether current segment is connected with previous 'prevG'
    bool isConnected = false;
    if (minSlope < curU.getSlope() && maxSlope > curL.getSlope())
    {

        Point ul = curU.getIntersection(&curL);
        isConnected = true;
        if (column_index == 1){
            std::cout << "    " << minSlope << " < " << curU.getSlope() << std::endl;
            std::cout << "    " << maxSlope << " > " << curL.getSlope() << std::endl;
            std::cout << "    isConnected = true;" << std::endl;
            ul.print();
        }

        // Update bounds
        if (maxSlope < curU.getSlope())
        {
            curU.update(&ul,maxSlope);
            std::cout << "    curU: ";
            curU.print();

        }
        if (minSlope > curL.getSlope())
        {
            curL.update(&ul,minSlope);
            std::cout << "    curL: ";
            curL.print();
        }
    }

    return isConnected;
}

// Find the fittest line in range of lower bound and upper bound
Line CoderSlideFilter::getFittestLine_G(int beginPoint, int endPoint, Line curU, Line curL)
{
    if (column_index == 1){
        std::cout << "CoderSlideFilter::getFittestLine_G(...)" << std::endl;
        std::cout << "    curU: ";
        curU.print();
        std::cout << "    curL: ";
        curL.print();

    }
    Point ul = curU.getIntersection(curL);
    if (column_index == 1){
        std::cout << "    ul = (" << ul.x << ", " << ul.y << ")" << std::endl;
    }
//    double numberator = 0;
//    double denominator = 0;
    float numberator = 0;
    float denominator = 0;

    for (int j = beginPoint + 1; j < endPoint;  j++)
    {
        DataItem item = m_pSFData->getAt(j);
        if (column_index == 1){
            std::cout << "    item = (" << item.timestamp << ", " << item.value << ")" << std::endl;
        }
        numberator += (item.value - ul.y) * (item.timestamp - ul.x);
        denominator += (item.timestamp - ul.x) * (item.timestamp - ul.x);
    }

//    double fraction = numberator / denominator;
//    double slopeU = curU.getSlope();
//    double slopeL = curL.getSlope();
    float fraction = numberator / denominator;
    float slopeU = curU.getSlope();
    float slopeL = curL.getSlope();
    if (column_index == 1){
        std::cout.precision(17);
        std::cout << "    numberator = " << numberator << std::endl;
        std::cout << "    denominator = " << denominator << std::endl;
        std::cout << "    fraction = " << fraction << std::endl;
        std::cout << "    slopeU = " << slopeU << std::endl;
        std::cout << "    slopeL = " << slopeL << std::endl;
    }

    // Get fittest slope in range of lower and upper bounds
//    double fittestSlope = fraction > slopeU ? slopeU : fraction;
    float fittestSlope = fraction > slopeU ? slopeU : fraction;
    fittestSlope = fittestSlope > slopeL ? fittestSlope : slopeL;

    // Create fittest line
    Line fittestLine;
    fittestLine.setSlope(fittestSlope);
    fittestLine.setIntercept(ul.y - fittestSlope * ul.x);
    if (column_index == 1){
        std::cout << "    fittestLine.setSlope(" << fittestSlope << ")" << std::endl;
        std::cout << "    fittestLine.setIntercept(" << ul.y - (fittestSlope * ul.x) << ")" << std::endl;
    }
    return fittestLine;
}

// Generate line segments for the filtering intervals and update the latest-executed point
void CoderSlideFilter::recording_mechanism(int& position)
{
    if (column_index == 1){
        std::cout << "CoderSlideFilter::recording_mechanism(...)" << std::endl;
    }
    int inputSize = m_pSFData->getDataLength();
////    m_curU.getIntersection(m_curL);
//    Point a = m_curU.getIntersection(m_curL);
//    if (column_index == 1) std::cout << "a = (" << a.x << ", " << a.y << ")" << std::endl;
    DataItem begin_curSeg = m_pSFData->getAt(m_nBegin_Point);

    bool existInter = updateUandLforConnectedSegment(m_curU,m_curL,m_prevG);

    m_curG = getFittestLine_G(m_nBegin_Point, position, m_curU, m_curL);

//    double t, eps;
    float t, eps;
    bool coded_entry = false;

    if (m_nBegin_Point == 0)
    {
        if (column_index == 1) std::cout << "    Create first recording" << std::endl;
        //Create first recording
        t = begin_curSeg.timestamp;
        codeEntry(true, t, m_curG.getValue(t));
        coded_entry = true;
    }
    else if (existInter)
    {
        if (column_index == 1) std::cout << "    m_curG cut m_prevG at valid section" << std::endl;
        //m_curG cut m_prevG at valid section
        Point inter = m_curG.getIntersection(m_prevG);

        // check if the decoder is able to reconstruct the original value
        if (m_pSFData->getEsp() == 0){
            Point p2 = m_curL.getPoint2();
            Point p2_float = Point((float) p2.y, (float) p2.x);

            Point inter_float = Point((float) inter.y, (float) inter.x);

            Line decodedLine(&inter_float, &p2_float);
            Point p1 = m_curU.getPoint1();

            int projection = (int) decodedLine.getValue(p1.x);
            if ((column_index == 1) && (projection !=  (int) p1.y)){
                std::cout << "DIFF" << std::endl;
                decodedLine.print();
                p1.print();
                std::cout << "projection = " << projection << std::endl;
                std::cout << "p1.y = " << p1.y << std::endl;
                std::cout << "(int) p1.y = " << (int) p1.y << std::endl;
            }
        }
        codeEntry(existInter, inter.x, inter.y);
        coded_entry = true;
    }
    if (!coded_entry)
    {
        if (column_index == 1) std::cout << "    m_curG cut m_prevG at invalid section" << std::endl;
        //m_curG cut m_prevG at invalid section
        DataItem end_prevSeg = m_pSFData->getAt(m_nBegin_Point - 1);
        t = end_prevSeg.timestamp;
        codeEntry(existInter, t, m_prevG.getValue(t));
        t = begin_curSeg.timestamp;
        codeEntry(true, t, m_curG.getValue(t));
    }

    if (position < inputSize -1)
    {
        if (column_index == 1) std::cout << "    Create new interval by two points" << std::endl;
        //Create new interval by two points
        m_nBegin_Point = position;
        DataItem curItem = m_pSFData->getAt(position);
        position++;
        DataItem nextItem = m_pSFData->getAt(position);
        eps = m_pSFData->getEsp();
        initializeU_L(curItem.timestamp, curItem.value, nextItem.timestamp, nextItem.value, eps);
        m_prevG = m_curG;
    }
    //if last interval has only one point --> Create last recording and finish compressing
    else if (position == (inputSize - 1))
    {
        if (column_index == 1) std::cout << "    Create last recording and finish compressing" << std::endl;
        m_nBegin_Point = position;
        DataItem preItem = m_pSFData->getAt(m_nBegin_Point - 1);
        DataItem item = m_pSFData->getAt(position);
        t = preItem.timestamp;
        codeEntry(true, t, m_curG.getValue(t));
        codeEntry(false, item.timestamp, item.value);
        position++;
//        std::cout << "  last_recording1 = (" << item.timestamp << ", " << item.value << ")" << std::endl;
    }
        //position == inputSize --> Create last recording
    else
    {
        if (column_index == 1) std::cout << "    Create last recording" << std::endl;
        DataItem item = m_pSFData->getAt(position - 1);
        t = item.timestamp;
        codeEntry(false, t, m_curG.getValue(t));
//        std::cout << "  last_recording2 = (" << item.timestamp << ", " << m_curG.getValue(t) << ")" << std::endl;
    }
}

// Adjust upper bound and lower bound with the arrival of each new data point at 'position'
void CoderSlideFilter::filtering_mechanism(int position)
{
    if (column_index == 1){
        std::cout << "CoderSlideFilter::filtering_mechanism(" << position << ")" << std::endl;
    }
    DataItem item = m_pSFData->getAt(position);
//    double upperValue = m_curU.getValue(item.timestamp);
//    double lowerValue = m_curL.getValue(item.timestamp);
    float upperValue = m_curU.getValue(item.timestamp);
    float lowerValue = m_curL.getValue(item.timestamp);
    int j;

//    double eps = m_pSFData->getEsp();
    float eps = m_pSFData->getEsp();
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

#endif // MASK_MODE
