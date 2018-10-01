
#ifndef CPP_PROJECT_TESTS_H
#define CPP_PROJECT_TESTS_H

#include <string>
#include "dataset.h"

class Tests {

public:
    static void runAll();

private:
    static void testDatasetUtils();
    static void testDatetimeUtils();
    static void testFloatCoder();
};

#endif //CPP_PROJECT_TESTS_H
