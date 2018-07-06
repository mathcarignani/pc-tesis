
#ifndef CPP_PROJECT_POINT_H
#define CPP_PROJECT_POINT_H

#include <iostream>

class CAPoint {

public:
    int x;
    int y;

    CAPoint(){
        x = 0;
        y = 0;
    }

    CAPoint(int x_, int y_){
        x = x_;
        y = y_;
    }

    CAPoint copy(){
        return CAPoint(x, y);
    }

    bool equal(CAPoint point){
        return point.x == x && point.y == y;
    }

//    void print(){
//        std::cout << "(x,y)=(" << std::to_string(x) << "," << std::to_string(y) << ")";
//    }
};

#endif //CPP_PROJECT_POINT_H
