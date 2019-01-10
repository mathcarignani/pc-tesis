#include "test.h"
using namespace std;

void Test::test_codigo_huffman() {
  printf("*********************************************\n");
  printf("************ TEST CODIGO HUFFMAN ************\n");
  printf("*********************************************\n");
  TestCodigoHuffman::test();
  printf("\n");
}

void Test::test_codigo_golomb(){
  printf("********************************************\n");
  printf("************ TEST CODIGO GOLOMB ************\n");
  printf("********************************************\n");
  printf("** TEST CODIGO **\n");
  TestCodigoGolomb::test_codigo();
  printf("** TEST LARGO **\n");
  TestCodigoGolomb::test_largo_codigo();
  printf("** TEST CODIGO ARCHIVO **\n");
  TestCodigoGolomb::test_codigo_archivo();
  printf("\n");
}

void Test::test_codigo_golomb_bn(){
  printf("***********************************************\n");
  printf("************ TEST CODIGO GOLOMB BN ************\n");
  printf("***********************************************\n");
  printf("** TEST ESPERANZA **\n");
  TestCodigoGolombBN::test_esperanza();
  printf("** TEST LARGO **\n");
  TestCodigoGolombBN::test_largo_codigo();
  printf("** TEST VECTOR LAMBDA **\n");
  TestCodigoGolombBN::test_vector_perm();
  printf("** TEST CODIGO ARCHIVO **\n");
  TestCodigoGolombBN::test_codigo_archivo();
  printf("\n");
}

void Test::test_codigo_t(){
  printf("***************************************\n");
  printf("************ TEST CODIGO T ************\n");
  printf("***************************************\n");
  printf("** TEST LARGO **\n");
  TestCodigoT::test_largo_codigo();
  printf("** TEST CODIGO ARCHIVO **\n");
  TestCodigoT::test_codigo_archivo();
  printf("\n");
}

void Test::todos_los_tests(){
  test_codigo_huffman();
  test_codigo_golomb();
  test_codigo_golomb_bn();
  test_codigo_t();
}
