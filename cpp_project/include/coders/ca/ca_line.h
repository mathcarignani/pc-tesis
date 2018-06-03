
#ifndef CPP_PROJECT_LINE_H
#define CPP_PROJECT_LINE_H

#include "ca_point.h"
#include "assert.h"
#include <iostream>

class CALine {

private:
    CAPoint point;
    double m;

    //
    // Returns the position of the point regarding the line.
    //
    int checkPoint(CAPoint other_point){
//        std::cout << "checkPoint(CAPoint other_point)" << std::endl;
//        other_point.print();
//        print();
        double y_inter = yIntersection(other_point);
//        std::cout << "y_inter = " << std::to_string(y_inter);
        if (y_inter == other_point.y) { // the point is inside the line
//            std::cout << "y_inter == other_point.y" << std::endl;
            return 0;
        }
        else if (y_inter > other_point.y ) { // the point is below the line
//            std::cout << "y_inter > other_point.y" << std::endl;
            return -1;
        }
        else { // the point is above the line
//            std::cout << "y_inter < other_point.y" << std::endl;
            return 1;
        }
    }

public:
    CALine(){
        point = CAPoint();
        m = 0;
    }

    //
    // PRE: point2.x > point1.x
    //
    CALine(CAPoint point1, CAPoint point2){
        assert(point2.x > point1.x);
        point = point1;
        if (point1.equal(point2)) { m = 0; }
        else {
            m = double(point2.y - point1.y) / point2.x;
        }
    }

    //
    // Returns the y coordinate of the intersection between self and the vertical line that passes through point.
    //
    double yIntersection(CAPoint other_point){
        return m * other_point.x + point.y;
    }

    bool pointBelowLine(CAPoint other_point){
        return checkPoint(other_point) == -1;
    }

    bool pointAboveLine(CAPoint other_point){
        return checkPoint(other_point) == 1;
    }

    static CALine sMin(CAPoint point1, CAPoint point2, int error_threshold){
        CAPoint point_minus_threshold = CAPoint(point2.x, point2.y - error_threshold);
        CALine line = CALine(point1.copy(), point_minus_threshold);
        return line;
    }

    static CALine sMax(CAPoint point1, CAPoint point2, int error_threshold){
        CAPoint point_plus_threshold = CAPoint(point2.x, point2.y + error_threshold);
        CALine line = CALine(point1.copy(), point_plus_threshold);
        return line;
    }

    void print(){
        std::cout << "(x,y,m)=(";
        std::cout << std::to_string(point.x) << "," << std::to_string(point.y) << "," << std::to_string(m) << ")";
    }
};

#endif //CPP_PROJECT_LINE_H
