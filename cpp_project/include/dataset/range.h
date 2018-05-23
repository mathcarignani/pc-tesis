
#ifndef CPP_PROJECT_RANGE_H
#define CPP_PROJECT_RANGE_H

#include <iostream>

struct Range {
    int begin;
    int end;

    Range() {
        begin = 0;
        end = 1;
    }

    Range(int b, int e) {
        begin = b;
        end = e;
    }

    bool insideRange(int value){
        return (begin <= value && value <= end);
    }

    void print(){
        std::cout << "Range = [" << begin << "," << end << "]" << std::endl;
    }
};

#endif //CPP_PROJECT_RANGE_H
