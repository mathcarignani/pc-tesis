
#include "pwlh_window.h"

#include "string_utils.h"


PWLHWindow::PWLHWindow(){}

PWLHWindow::PWLHWindow(int max_window_size_, int error_threshold_, Range range_, bool integer_mode_){
    max_window_size = max_window_size_;
    max_window_size_bit_length = StringUtils::bitLength(max_window_size);
    error_threshold = error_threshold_;
    range = range_;
    bucket = new LinearBucket(error_threshold);
    length = 0;
    nan_window = false;
    integer_mode = integer_mode_;
}

bool PWLHWindow::conditionHolds(std::string x){
    if (isEmpty()){ // this condition is only true the first time this method is called
        addFirstValue(x);
        return true;
    }
    else if (isFull()){
        return false;
    }
    else if (x[0] == 'N'){
        if (nan_window){ length++; return true;  }
        else {                     return false; }
    }
    else { // x is an integer
        if (nan_window) { return false; }
        else {
            int x_int = std::stoi(x);
            bucket->addPoint(x_int);
            if (bucket->checkEpsConstraint() && checkIntegerModeConstraint()){ // bucket is valid
//                std::cout << "BUCKET IS VALID" << std::endl;
                length++;
                return true;
            }
            else { // bucket is invalid
//                std::cout << "ELSE" << std::endl;
                bucket->removePoint();
                bucket->getAproximatedLine(p1, p2);
                p1.x = 0;
                p2.x = length - 1; // TODO: consider time delta column
//                std::cout << "p1=(x,y)=" << p1.x << "," << p1.y << std::endl;
//                std::cout << "p2=(x,y)=" << p2.x << "," << p2.y << std::endl;
                return false;
            }
        }
    }
}

bool PWLHWindow::checkIntegerModeConstraint(){
    bucket->getAproximatedLine(p1, p2);
    if (!integer_mode) { return true; }
    // this constraint is only checked when running in integer mode
//    bucket->getAproximatedLine(p1, p2);
    return range.insideRange(StringUtils::doubleToInt(p1.y)) && range.insideRange(StringUtils::doubleToInt(p2.y));
}

bool PWLHWindow::isFull(){
    return length == max_window_size;
}

bool PWLHWindow::isEmpty(){
    return length == 0;
}

void PWLHWindow::addFirstValue(std::string x){
    length = 1;
    if (x[0] == 'N'){
        nan_window = true;
        constant_value = "N";
        constant_value_float = 0; // doesn't matter
    }
    else { // x is an integer
        nan_window = false;
        int x_int = std::stoi(x);
        if (bucket->getSize() != 0) { bucket->resetBucket(); }
//        std::cout << "addFirstValue ELSE " << x_int << std::endl;
        bucket->addPoint((double) x_int);
        constant_value = x;
        constant_value_float = (float) x_int;
    }
}

float PWLHWindow::getPoint1Y(){
//    std::cout << "p1.y = " << p1.y << std::endl;
    return p1.y;
}

float PWLHWindow::getPoint2Y(){
//    std::cout << "p2.y = " << p2.y << std::endl;
    return p2.y;
}

std::string PWLHWindow::getPoint1YIntegerMode(){
//    std::cout << "p1.y = " << p1.y << std::endl;
    return StringUtils::doubleToString(p1.y);
}

std::string PWLHWindow::getPoint2YIntegerMode(){
//    std::cout << "p2.y = " << p2.y << std::endl;
    return StringUtils::doubleToString(p2.y);
}

std::vector<std::string> PWLHWindow::decodePoints(float point1_y, float point2_y, int window_size){
//    std::cout << "A<point1_y_int, point2_y_int> = " << point1_y_int << ", " << point2_y_int << ">" << std::endl;
    Point p1 = Point(point1_y, 0);
    Point p2 = Point(point2_y, window_size-1); // TODO: consider time delta column
    Line* line = new Line(&p1, &p2);
//    std::cout << "B<point1_y_int, point2_y_int> = " << line->getValue(0) << ", " << line->getValue(window_size-1) << ">" << std::endl;

    return proyectPointsOntoLine(line, window_size);
}

std::vector<std::string> PWLHWindow::decodePointsIntegerMode(std::string point1_y, std::string point2_y, int window_size){
    int point1_y_int = std::stoi(point1_y);
    int point2_y_int = std::stoi(point2_y);
//    std::cout << "A<point1_y_int, point2_y_int> = " << point1_y_int << ", " << point2_y_int << ">" << std::endl;
    Point p1 = Point(point1_y_int, 0);
    Point p2 = Point(point2_y_int, window_size-1); // TODO: consider time delta column
    Line* line = new Line(&p1, &p2);
//    std::cout << "B<point1_y_int, point2_y_int> = " << line->getValue(0) << ", " << line->getValue(window_size-1) << ">" << std::endl;

    return proyectPointsOntoLine(line, window_size);
}

std::vector<std::string> PWLHWindow::proyectPointsOntoLine(Line* line, int window_size){
    // TODO: consider time delta column
    std::vector<std::string> res(window_size);
    for (int i=0; i < window_size; i++){
        double value = line->getValue(i);
        res[i] = StringUtils::doubleToString(value);
    }
    return res;
}