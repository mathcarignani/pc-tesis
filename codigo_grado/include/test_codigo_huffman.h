#ifndef __TEST_CODIGO_HUFFMAN_H__
#define __TEST_CODIGO_HUFFMAN_H__

#include "codigo_huffman.h"
#include "test_aux.h"

class TestCodigoHuffman { 

private:

static std::vector <double> crear_probabilidades(double probs[], int cant_simbolos);

static bool comparar_codigos(std::vector <PalabraDeCodigo*> codigo_huffman_1, 
                             CodigoHuffman* codigo_huffman_2);

static void test_huffman(int enteros[], int largos[], double probs[],
                         int cant_simbolos, int numero_test);

public:

static void test();

};

#endif
