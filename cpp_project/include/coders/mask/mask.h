
#ifndef CPP_PROJECT_MASK_H
#define CPP_PROJECT_MASK_H

#include <vector>

class Burst {

public:
    bool no_data;
    int length;

    Burst(bool no_data_, int length_){
        no_data = no_data_;
        length = length_;
    }
};

class Mask {

private:
    // creation variables
    std::vector<Burst*> bursts;

    // iteration variables
    int current_index;
    bool burst_is_no_data;
    int burst_length;

    void setBurst(int index){
        Burst* burst = bursts.at(index);
        burst_is_no_data = burst->no_data;
        burst_length = burst->length;
    }

public:
    int total_no_data; // number of "nodata" entries
    int total_data; // number of non-"nodata" entries

    Mask(){
        bursts.clear();
        total_no_data = 0;
        total_data = 0;
    }

    void add(bool burst_is_no_data_, int burst_length_){
        bursts.push_back(new Burst(burst_is_no_data_, burst_length_));
        if (burst_is_no_data_) { total_no_data += burst_length_; } else { total_data += burst_length_; }
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

#endif //CPP_PROJECT_MASK_H
