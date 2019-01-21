
#include "mask.h"

Mask::Mask(){
    total_no_data = 0;
    total_data = 0;
    bursts.clear();
}

void Mask::setBurst(int index){
    assert(index < bursts.size());
    Burst* burst = bursts.at(index);
    burst_is_no_data = burst->no_data;
    burst_length = burst->length;
}

void Mask::add(Burst* burst){
    bursts.push_back(burst);
    if (burst->no_data) { total_no_data += burst->length; } else { total_data += burst->length; }
}

void Mask::add(bool no_data, int length){
    add(new Burst(no_data, length));
}

void Mask::reset(){
    current_index = 0;
    setBurst(0);
}

bool Mask::isNoData(){
    if (burst_length == 0){
        current_index++;
        setBurst(current_index);
    }
    burst_length--;
    return burst_is_no_data;
}