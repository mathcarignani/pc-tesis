
#ifndef CPP_PROJECT_MASK_H
#define CPP_PROJECT_MASK_H

#include <vector>
#include <iostream>
#include <assert.h>

class Mask {

protected:
    int current_index; // iteration variable

public:
    int total_no_data; // number of "nodata" entries
    int total_data; // number of non-"nodata" entries

    Mask(){
        total_no_data = 0;
        total_data = 0;
    }

    virtual void reset() = 0;
    virtual bool isNoData() = 0;
};

#endif //CPP_PROJECT_MASK_H
