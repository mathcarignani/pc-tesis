
#include "tests_string_utils.h"
#include "string_utils.h"
#include <cassert>
#include <iostream>

void TestsStringUtils::runAll(){
    std::cout << "  splitByCharWithIndexTest();" << std::endl; splitByCharWithIndexTest();
    std::cout << "  charToIntTest();" << std::endl;            charToIntTest();
    std::cout << "  intToCharTest();" << std::endl;            intToCharTest();
}

void TestsStringUtils::splitByCharWithIndexTest(){

    std::string line = "60,N,N,N,N,N,N,N,N,N,N\r";
    assert(StringUtils::splitByCharWithIndex(line, ',', 0) == "60");
    assert(StringUtils::splitByCharWithIndex(line, ',', 1) == "N");
    assert(StringUtils::splitByCharWithIndex(line, ',', 9) == "N");
    assert(StringUtils::splitByCharWithIndex(line, ',', 10) == "N\r");
    assert(StringUtils::splitByCharWithIndex(line, ',', 11) == "");
}

void TestsStringUtils::charToIntTest(){
    assert(StringUtils::charToInt('A') == 65);
    assert(StringUtils::charToInt('Z') == 90);
    assert(StringUtils::charToInt('a') == 97);
    assert(StringUtils::charToInt('z') == 122);
}

void TestsStringUtils::intToCharTest(){
    assert(StringUtils::intToChar(65) == 'A');
    assert(StringUtils::intToChar(90) == 'Z');
    assert(StringUtils::intToChar(97) == 'a');
    assert(StringUtils::intToChar(122) == 'z');
}
