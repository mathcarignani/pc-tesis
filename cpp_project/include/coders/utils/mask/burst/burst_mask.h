
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

    void setBurst(int index){
        assert(index < bursts.size());
        Burst* burst = bursts.at(index);
        burst_is_no_data = burst->no_data;
        burst_length = burst->length;
    }

public:
    BurstMask(): Mask(){
        bursts.clear();
    }

    void add(Burst* burst){
        bursts.push_back(burst);
        if (burst->no_data) { total_no_data += burst->length; } else { total_data += burst->length; }
    }

    void reset(){
        current_index = 0;
        setBurst(0);
    }

    bool isNoData(){
        if (burst_length == 0){
            current_index++;
            setBurst(current_index);
        }
        burst_length--;
        return burst_is_no_data;
    }
};

#endif //CPP_PROJECT_BURST_MASK_H
