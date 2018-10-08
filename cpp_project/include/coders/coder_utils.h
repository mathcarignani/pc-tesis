
#ifndef CPP_PROJECT_CODER_UTILS_H
#define CPP_PROJECT_CODER_UTILS_H

#include <vector>
#include <string>
#include "constants.h"
#include <assert.h>
#include "mask.h"
#include <iostream>

class CoderUtils {

public:
    static std::vector<int> createXCoordsVector(std::vector<int> time_delta_vector, int window_size, int row_index);
    static std::vector<int> createXCoordsVector(Mask* mask, std::vector<int> time_delta_vector, int window_size);
#if MASK_MODE
    static std::vector<int> createXCoordsVectorMaskMode(Mask* mask, std::vector<int> time_delta_vector, int init_delta_sum);
#endif
};

class Column {

public:
    std::vector<std::string> column_vector;
    int row_index;
    int unprocessed_rows;
    int unprocessed_data_rows;
    int unprocessed_no_data_rows;

#if MASK_MODE
    Column(int unprocessed_rows_, int total_data, int total_no_data){
        row_index = 0;
        unprocessed_rows = unprocessed_rows_;
        unprocessed_data_rows = total_data;
        unprocessed_no_data_rows = total_no_data;
        assert(unprocessed_rows = unprocessed_data_rows + unprocessed_no_data_rows);
    }

    void addData(std::string value){
        addValue(value);
        unprocessed_data_rows--;
    }

    void addNoData(){
        addValue(Constants::NO_DATA);
        unprocessed_no_data_rows--;
    }

    void assertAfter(){
        assert(unprocessed_rows == 0);
        assert(unprocessed_data_rows == 0);
        assert(unprocessed_no_data_rows == 0);
    }
#else
    Column(int unprocessed_rows_){
        row_index = 0;
        unprocessed_rows = unprocessed_rows_;
    }

    void addData(std::string value){
        addValue(value);
    }

    void addNoData(){
        addValue(Constants::NO_DATA);
    }

    void assertAfter(){
        assert(unprocessed_rows == 0);
    }
#endif

private:
    void addValue(std::string value){
        column_vector.push_back(value);
        row_index++;
        unprocessed_rows--;
    }
};

#endif //CPP_PROJECT_CODER_UTILS_H
