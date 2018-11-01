
#include "tests_line.h"
#include "assert.h"
#include <iostream>

void TestsLine::runAll(){
    std::cout << "  getValueTest()" << std::endl; getValueTest();
}

void TestsLine::getValueTest(){
    Line* line1 = new Line(new Point(430, 0), new Point(428, 2));
    assert(line1-> getValue(1) == 429);

    int num = 103620;
    Line* line2 = new Line(new Point(430, num), new Point(428, num + 60*2));
    assert(line2-> getValue(num + 60) == 429);
}
