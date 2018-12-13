
#ifndef CPP_PROJECT_COLUMN_H
#define CPP_PROJECT_COLUMN_H

#include <assert.h>

class Column {

public:
    std::vector<std::string> column_vector;
    int row_index;
    int unprocessed_data_rows;
    int unprocessed_no_data_rows;
    int processed_data_rows;

    bool notFinished(){
        return unprocessed_rows > 0;
    }

#if MASK_MODE
    Column(int unprocessed_rows_, int total_data, int total_no_data){
        row_index = 0;
        unprocessed_rows = unprocessed_rows_;
        unprocessed_data_rows = total_data;
        unprocessed_no_data_rows = total_no_data;
        assert(unprocessed_rows = unprocessed_data_rows + unprocessed_no_data_rows);
        processed_data_rows = 0;
    }

    void addData(std::string value){
//        std::cout << "I=" << row_index << "-----------------------------> " << value << std::endl;
        addValue(value);
        unprocessed_data_rows--;
        processed_data_rows++;
    }

    void addNoData(){
//        std::cout << "I=" << row_index << "-----------------------------> NO DATA" << std::endl;
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

    void addDataXTimes(std::string value, int x){
        for (int i=0; i < x; i++) { addValue(value); }
    }

    void addNoData(){
        addValue(Constants::NO_DATA);
    }

    void addNoDataXTimes(int x){
        for (int i=0; i < x; i++) { addValue(Constants::NO_DATA); }
    }

    void addDataVector(std::vector<std::string> values){
        for (int i=0; i < values.size(); i++) { addValue(values.at(i)); }
    }

    void assertAfter(){
        assert(unprocessed_rows == 0);
    }
#endif

private:
    int unprocessed_rows;

    void addValue(std::string value){
        column_vector.push_back(value);
        row_index++;
        unprocessed_rows--;
    }
};

#endif //CPP_PROJECT_COLUMN_H
