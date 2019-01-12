
#ifndef CPP_PROJECT_BURST_MASK_H
#define CPP_PROJECT_BURST_MASK_H

#include "mask.h"
#include "burst.h"

class BurstMask: public Mask {

private:
    // creation variables
    std::vector<Burst*> bursts;

    // iteration variables
    bool burst_is_no_data;
    int burst_length;

    void setBurst(int index);

public:
    BurstMask();
    void add(Burst* burst);
    void reset();
    bool isNoData();
};

#endif //CPP_PROJECT_BURST_MASK_H
