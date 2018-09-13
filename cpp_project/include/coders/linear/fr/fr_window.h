
#ifndef CPP_PROJECT_FR_WINDOW_H
#define CPP_PROJECT_FR_WINDOW_H

#include "DataItem.h"
#include <vector>
#include <string>

class FRWindow {

private:
    std::vector<DataItem> data;
    int max_window_size;
    int error_threshold;
    int length;
    void getIndexes(std::vector<int> & array, int first_index, int last_index);
    bool violatedConstraint(int first_index, int last_index);

public:
    FRWindow();
    FRWindow(int max_window_size_, int error_threshold_);

    void addDataItem(int timestamp, std::string value);
    bool isFull();
    bool isEmpty();
    void clear();
    std::vector<DataItem> getItems();

};
#endif //CPP_PROJECT_FR_WINDOW_H
