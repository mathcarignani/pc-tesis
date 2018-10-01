
#include "tests_math_utils.h"
#include "math_utils.h"
#include <cassert>
#include <iostream>

void TestsMathUtils::runAll(){
    bitLengthTest();
    doubleToIntTest();
    intAbsoluteTest();
    doubleAbsoluteTest();
    halfTest();
}

void TestsMathUtils::bitLengthTest(){
    std::cout << "TestsMathUtils::bitLengthTest()..." << std::endl;
    assert(MathUtils::bitLength(0) == 1);
    assert(MathUtils::bitLength(1) == 1);
    assert(MathUtils::bitLength(2) == 2);
    assert(MathUtils::bitLength(3) == 2);
    assert(MathUtils::bitLength(4) == 3);
}

void TestsMathUtils::doubleToIntTest(){
    std::cout << "TestsMathUtils::bitLengthTest()..." << std::endl;
    double double1, double2, double3;
    double1 = -50; double2 = 0; double3 = 50;
    assert(MathUtils::doubleToInt(double1) == -50);
    assert(MathUtils::doubleToInt(double2) == 0);
    assert(MathUtils::doubleToInt(double3) == 50);
}

void TestsMathUtils::intAbsoluteTest(){
    std::cout << "TestsMathUtils::intAbsoluteTest()..." << std::endl;
    assert(MathUtils::intAbsolute(-50) == 50);
    assert(MathUtils::intAbsolute(0) == 0);
    assert(MathUtils::intAbsolute(50) == 50);
}

void TestsMathUtils::doubleAbsoluteTest(){
    std::cout << "TestsMathUtils::doubleAbsoluteTest()..." << std::endl;
    assert(MathUtils::doubleAbsolute(-50.8) == 50.8);
    assert(MathUtils::doubleAbsolute(0) == 0);
    assert(MathUtils::doubleAbsolute(50.8) == 50.8);
}

void TestsMathUtils::halfTest(){
    std::cout << "TestsMathUtils::halfTest()..." << std::endl;
    assert(MathUtils::half(0, 0) == 0);
    assert(MathUtils::half(0, 1) == 0);
    assert(MathUtils::half(1, 1) == 1);
    assert(MathUtils::half(0, 2) == 1);
}
