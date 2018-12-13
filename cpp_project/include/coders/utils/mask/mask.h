
#ifndef CPP_PROJECT_MASK_H
#define CPP_PROJECT_MASK_H

#include <vector>
#include <iostream>
#include <assert.h>

class Burst {

public:
    bool no_data;
    int length;

    Burst(bool no_data_){
        no_data = no_data_;
        length = 1;
    }

    Burst(bool no_data_, int length_){
        no_data = no_data_;
        length = length_;
    }

    void increaseLength(){
        length++;
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
        assert(index < bursts.size());
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

    void add(Burst* burst){
        bursts.push_back(burst);
        if (burst->no_data) { total_no_data += burst->length; } else { total_data += burst->length; }
    }

    void reset(){
        current_index = 0;
        setBurst(0);
    }

    bool isNoData(){
//        std::cout << "BEGIN isNoData" << std::endl;
        if (burst_length == 0){
            current_index++;
            setBurst(current_index);
        }
        burst_length--;
//        std::cout << "END isNoData" << std::endl;
        return burst_is_no_data;
    }
};

#endif //CPP_PROJECT_MASK_H
