
#include "tests_bit_stream.h"
#include <cfloat>
#include "assert.h"
#include <iostream>
#include "tests_utils.h"

void TestsBitStream::runAll(){
    std::cout << "  floatTest();" << std::endl;
    floatTest();
}

void TestsBitStream::floatTest(){
    Path coded_path = Path(TestsUtils::OUTPUT_PATH, "testFloat.code");
    BitStreamWriter* bit_stream_writer = new BitStreamWriter(coded_path);
    float a = 0.238728932739; bit_stream_writer->pushFloat(a);
    float b = 0.2893232; bit_stream_writer->pushFloat(b);
    float c = 203020323.22; bit_stream_writer->pushFloat(c);
    float d = FLT_MAX; bit_stream_writer->pushFloat(d);
    delete bit_stream_writer;

    BitStreamReader* bit_stream_reader = new BitStreamReader(coded_path);
    float diff = 0.00000000000000000000000000000001;
    float a_deco = bit_stream_reader->getFloat(); assert(a_deco - a < diff);
    float b_deco = bit_stream_reader->getFloat(); assert(b_deco - b < diff);
    float c_deco = bit_stream_reader->getFloat(); assert(c_deco - c < diff);
    float d_deco = bit_stream_reader->getFloat(); assert(d_deco == d);
    delete bit_stream_reader;
}
