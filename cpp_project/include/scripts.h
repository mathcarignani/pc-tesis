
#ifndef CPP_PROJECT_SCRIPTS_H
#define CPP_PROJECT_SCRIPTS_H

#include <string>
#include "path.h"
#include <vector>
#include "dataset.h"
#include "constants.h"

class Scripts {

public:
    static void decode(Path input_path, Path output_path);

    static Dataset* codeBase(Path input_path, Path output_path);
    static Dataset* code(std::string coder_name, Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector);

private:
    static Dataset* codePCA(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector);
    static Dataset* codeAPCA(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector);
    static Dataset* codePWLH(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector, bool integer_mode);
    static Dataset* codeCA(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector);
#if MASK_MODE
    static Dataset* codeSF(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector);
    static Dataset* codeFR(Path input_path, Path output_path, int window_size, std::vector<int> error_thresholds_vector);
#endif
    static Dataset* codeGAMPS(Path input_path, Path output_path, int window_size,
                              std::vector<int> error_thresholds_vector, bool limit_mode);
};

#endif //CPP_PROJECT_SCRIPTS_H
