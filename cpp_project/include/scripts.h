
#ifndef CPP_PROJECT_SCRIPTS_H
#define CPP_PROJECT_SCRIPTS_H

#include <string>
#include "path.h"
#include <vector>
#include "dataset.h"
#include "constants.h"

class Scripts {

public:
    static Dataset* codeBasic(Path input_path, Path output_path);
    static void decodeBasic(Path input_path, Path output_path);

    static Dataset* codePCA(Path input_path, Path output_path, int fixed_window_size, std::vector<int> error_thresholds_vector);
    static void decodePCA(Path input_path, Path output_path, int fixed_window_size);

    static Dataset* codeAPCA(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector);
    static void decodeAPCA(Path input_path, Path output_path, int max_window_size);

    static Dataset* codePWLH(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector, bool integer_mode);
    static void decodePWLH(Path input_path, Path output_path, int max_window_size, bool integer_mode);

    static Dataset* codeCA(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector);
    static void decodeCA(Path input_path, Path output_path, int max_window_size);

#if MASK_MODE
    static Dataset* codeSF(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector);
    static void decodeSF(Path input_path, Path output_path, int max_window_size);

    static Dataset* codeFR(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector);
    static void decodeFR(Path input_path, Path output_path, int max_window_size);

    static Dataset* codeGAMPS(Path input_path, Path output_path, int max_window_size, std::vector<int> error_thresholds_vector);
    static void decodeGAMPS(Path input_path, Path output_path, int max_window_size);
#endif
};

#endif //CPP_PROJECT_SCRIPTS_H
