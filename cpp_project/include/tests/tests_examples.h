
#ifndef CPP_PROJECT_TESTS_EXAMPLES_H
#define CPP_PROJECT_TESTS_EXAMPLES_H

#include <iostream>


class TestsExamples {
public:
    static void runAll();

private:
    static void pcaTest();

    static const std::string EXAMPLES_PATH;
    static const std::string EXPECTED_PATH;
    static const std::string OUTPUT_PATH;

};

#endif //CPP_PROJECT_TESTS_EXAMPLES_H
