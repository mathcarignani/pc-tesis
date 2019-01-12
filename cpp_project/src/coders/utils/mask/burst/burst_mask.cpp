
#include "burst_mask.h"

BurstMask::BurstMask(): Mask(){
    bursts.clear();
}

void BurstMask::setBurst(int index){
    assert(index < bursts.size());
    Burst* burst = bursts.at(index);
    burst_is_no_data = burst->no_data;
    burst_length = burst->length;
}

void BurstMask::add(Burst* burst){
    bursts.push_back(burst);
    if (burst->no_data) { total_no_data += burst->length; } else { total_data += burst->length; }
}

void BurstMask::reset(){
    current_index = 0;
    setBurst(0);
}

bool BurstMask::isNoData(){
    if (burst_length == 0){
        current_index++;
        setBurst(current_index);
    }
    burst_length--;
    return burst_is_no_data;
}
