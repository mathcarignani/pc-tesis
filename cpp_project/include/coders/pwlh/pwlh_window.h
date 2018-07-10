
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
    bool integer_mode;

public:
    int max_window_size_bit_length;
    int length;
    bool nan_window;
    std::string constant_value;
    float constant_value_float;
    Point p1;
    Point p2;

    PWLHWindow();
    PWLHWindow(int max_window_size_, int error_threshold_, Range range_, bool integer_mode_);
    bool conditionHolds(std::string x);
    bool checkIntegerModeConstraint();
    bool isFull();
    bool isEmpty();
    void addFirstValue(std::string x);
    float getPoint1Y();
    float getPoint2Y();
    std::string getPoint1YIntegerMode();
    std::string getPoint2YIntegerMode();

    static std::vector<std::string> decodePoints(float point1_y, float point2_y, int window_size);
    static std::vector<std::string> decodePointsIntegerMode(std::string point1_y, std::string point2_y, int window_size);
    static std::vector<std::string> proyectPointsOntoLine(Line* line, int window_size);
};

#endif //CPP_PROJECT_PWLH_WINDOW_H
