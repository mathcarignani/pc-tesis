
#ifndef CPP_PROJECT_PWLH_WINDOW_H
#define CPP_PROJECT_PWLH_WINDOW_H

#include <string>
#include "LinearBucket.h"
#include "range.h"

class PWLHWindow {

private:
    int max_window_size;
    int error_threshold;
    LinearBucket* bucket;
    Range range;

public:
    int max_window_size_bit_length;
    int length;
    bool nan_window;
    std::string constant_value;
    Point p1;
    Point p2;

    PWLHWindow(int max_window_size_, int error_threshold_, Range range_);
    bool conditionHolds(std::string x);
    bool checkAdditionalBucketConstraint();
    bool isFull();
    bool isEmpty();
    void addFirstValue(std::string x);
    std::string getPoint1Y();
    std::string getPoint2Y();

    static std::vector<std::string> decodePoints(std::string point1_y, std::string point2_y, int window_size);
};

#endif //CPP_PROJECT_PWLH_WINDOW_H
