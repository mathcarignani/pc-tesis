
#ifndef CPP_PROJECT_GAMPS_UTILS_H
#define CPP_PROJECT_GAMPS_UTILS_H

#include <string>
#include "dataset.h"

class GAMPSUtils {
public:
    static std::vector<int> columnGroupIndexes(Dataset* dataset, int group_index);
};

#endif //CPP_PROJECT_GAMPS_UTILS_H
