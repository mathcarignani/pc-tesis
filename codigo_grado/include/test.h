#ifndef __TEST_H__
#define __TEST_H__

#include "test_codigo_golomb.h"
#include "test_codigo_golomb_bn.h"
#include "test_codigo_huffman.h"
#include "test_codigo_t.h"

class Test {

public:
  static void test_codigo_huffman();
  static void test_codigo_golomb();
  static void test_codigo_golomb_bn();
  static void test_codigo_t();
  static void todos_los_tests();

};

#endif
