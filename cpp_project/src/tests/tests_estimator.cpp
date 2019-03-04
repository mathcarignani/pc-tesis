
#include "tests_estimator.h"
#include "estimator.h"
#include "assert.h"
#include <iostream>

TestsEstimator::TestsEstimator(){ }

void TestsEstimator::runAll(){
    std::cout << "  testEstimateProbability()" << std::endl; testEstimateProbability();
}

void TestsEstimator::testEstimateProbability(){
    Estimator* estimator = new Estimator();
    estimator->print();
    assert(estimator->estimateProbability(true) == (0 + 0.5) / 1);  // 0_1
    assert(estimator->estimateProbability(true) == (0 + 0.5) / 1);  // 0_11
    assert(estimator->estimateProbability(true) == (1 + 0.5) / 2);  // 0_111
    assert(estimator->estimateProbability(true) == (2 + 0.5) / 3);  // 0_111
    assert(estimator->estimateProbability(true) == (3 + 0.5) / 4);  // 0_1111
    assert(estimator->estimateProbability(false) == (0 + 0.5) / 5); // 0_11110
    assert(estimator->estimateProbability(true) == (1 + 0.5) / 2);  // 0_111101
    assert(estimator->estimateProbability(false) == (1 + 0.5) / 6); // 0_1111010
    assert(estimator->estimateProbability(false) == (0 + 0.5) / 3); // 0_11110100
};
