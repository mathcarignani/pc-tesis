
#ifndef CPP_PROJECT_SCRIPTS_H
#define CPP_PROJECT_SCRIPTS_H

#include <string>
#include "path.h"
#include <vector>
#include "dataset.h"
#include "constants.h"

class Scripts {

public:
    static Dataset* code(std::string coder_name,
                         Path input_path,
                         Path output_path,
                         int window_size,
                         std::vector<int> error_thresholds_vector);
    static void decode(Path input_path, Path output_path);

};

#endif //CPP_PROJECT_SCRIPTS_H
