
#ifndef CPP_PROJECT_MASK_H
#define CPP_PROJECT_MASK_H

#include <vector>

class Mask {

private:
    // creation variables
    std::vector<bool> burst_is_no_data_vector;
    std::vector<int> burst_length_vector;

    // iteration variables
    int current_index;
    bool burst_is_no_data;
    int burst_length;

public:
    int total_no_data; // number of "nodata" entries
    int total_data; // number of non-"nodata" entries

    Mask(){
        burst_is_no_data_vector.clear();
        burst_length_vector.clear();
        total_no_data = 0;
        total_data = 0;
    }

    void add(bool burst_is_no_data_, int burst_length_){
        burst_is_no_data_vector.push_back(burst_is_no_data_);
        burst_length_vector.push_back(burst_length_);
        if (burst_is_no_data_) { total_no_data += burst_length_; } else { total_data += burst_length_; }
    }

    void reset(){
        current_index = 0;
        burst_is_no_data = burst_is_no_data_vector.at(0);
        burst_length = burst_length_vector.at(0);
    }

    bool isNoData(){
        if (burst_length == 0){
            current_index++;
            burst_is_no_data = burst_is_no_data_vector.at(current_index);
            burst_length = burst_length_vector.at(current_index);
            // std::cout << "burst_length = " << burst_length << std::endl;
            // std::cout << (burst_is_no_data ? "1" : "0") << std::endl;
        }
        burst_length--;
        // std::cout << " " << (burst_is_no_data ? "nodata" : "data") << std::endl;
        return burst_is_no_data;
    }
};

#endif //CPP_PROJECT_MASK_H
