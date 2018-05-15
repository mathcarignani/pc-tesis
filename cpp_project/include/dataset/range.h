
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
};

#endif //CPP_PROJECT_RANGE_H
