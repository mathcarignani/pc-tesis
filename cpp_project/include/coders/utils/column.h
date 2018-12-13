
#ifndef CPP_PROJECT_COLUMN_H
#define CPP_PROJECT_COLUMN_H

#include <assert.h>

class Column {

private:
    int unprocessed_rows;

    void addValue(std::string value){
        column_vector.push_back(value);
        row_index++;
        unprocessed_rows--;
    }

public:
    std::vector<std::string> column_vector;
    int row_index;
    int unprocessed_data_rows;
    int unprocessed_no_data_rows;
    int processed_data_rows;

    bool notFinished(){
        return unprocessed_rows > 0;
    }

    void addData(std::string value){
//        std::cout << "I=" << row_index << "-----------------------------> " << value << std::endl;
        addValue(value);
    #if MASK_MODE
        unprocessed_data_rows--;
        processed_data_rows++;
    #endif
    }

    void addNoData(){
//        std::cout << "I=" << row_index << "-----------------------------> NO DATA" << std::endl;
        addValue(Constants::NO_DATA);
    #if MASK_MODE
        unprocessed_no_data_rows--;
    #endif
    }

    void assertAfter(){
        assert(unprocessed_rows == 0);
    #if MASK_MODE
        assert(unprocessed_data_rows == 0);
        assert(unprocessed_no_data_rows == 0);
    #endif
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
#else
    Column(int unprocessed_rows_){
        row_index = 0;
        unprocessed_rows = unprocessed_rows_;
    }

    void addDataXTimes(std::string value, int x){
        for (int i=0; i < x; i++) { addValue(value); }
    }

    void addNoDataXTimes(int x){
        for (int i=0; i < x; i++) { addValue(Constants::NO_DATA); }
    }

    void addDataVector(std::vector<std::string> values){
        for (int i=0; i < values.size(); i++) { addValue(values.at(i)); }
    }
#endif // MASK_MODE

};

#endif //CPP_PROJECT_COLUMN_H
