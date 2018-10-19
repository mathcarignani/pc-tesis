
#ifndef CPP_PROJECT_SLIDE_FILTER_WINDOW_H
#define CPP_PROJECT_SLIDE_FILTER_WINDOW_H

#include <string>
#include <vector>
#include "Line.h"


class SlideFilterWindow {

private:
    std::vector<DataItem> data;
    int error_threshold;
    int total_data_rows;

public:
    int length;
    SlideFilterWindow();
    SlideFilterWindow(int total_data_rows_, int error_threshold_);
    void addDataItem(int timestamp, std::string value);
    int getDataLength();
    DataItem getAt(int pos);
    int getEsp();
//    int getPosition(int timestamp);

};

#endif //CPP_PROJECT_SLIDE_FILTER_WINDOW_H

//#ifndef CPP_PROJECT_SLIDE_FILTER_WINDOW_H
//#define CPP_PROJECT_SLIDE_FILTER_WINDOW_H
//
//#include <string>
//#include <vector>
//#include "Line.h"
//
//class SlideFilterWindow {
//
//private:
//    int window_size;
//    int total_data_rows;
//    int error_threshold;
//    bool initialized;
//
//    double upperValue, lowerValue;
//
//    void initializeU_L(int t1, int v1, int t2, int v2);
//    void filtering_mechanism(int position);
//    void recording_mechanism(int & position);
//    bool updateUandLforConnectedSegment(Line& curU, Line& curL, Line prevG);
//
//public:
//    int window_size_bit_length;
//    int length;
//
//    int m_nBegin_Point;
//    std::vector<int> window_values;
//    std::vector<int> window_deltas;
//
//    Line m_curU;// Upper bound line
//    Line m_curL;// Lower bound line
//    Line m_curG;// Current segment
//    Line m_prevG;// Previous segment
//
//    SlideFilterWindow();
//    SlideFilterWindow(int window_size_, int error_threshold_, int total_data_rows_);
//    bool addValue(std::string x, int x_delta);
//
//    void printLine(std::string name, Line &line);
//    bool updateUandLforConnectedSegment(int m_nBegin_Point, Line& curU, Line& curL, Line prevG);
//    Line getFittestLine_G(int beginPoint, int endPoint, Line curU, Line curL)
//
//
//};
//
//#endif //CPP_PROJECT_SLIDE_FILTER_WINDOW_H
