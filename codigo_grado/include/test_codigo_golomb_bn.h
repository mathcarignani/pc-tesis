#ifndef __TEST_CODIGO_GOLOMB_BN_H__
#define __TEST_CODIGO_GOLOMB_BN_H__

#include "codigo_golomb_bn.h"
#include "distribucion_bn.h"
#include "test_aux.h"

class TestCodigoGolombBN { 

private:

static void test_largo_codigo_aux(int numero_test, double p);

static void test_codigo_archivo_aux(int numero_test, double p, int cant_repeticiones);

public:

// testea que el largo de codigo calculado analiticamente
// es igual al largo de codigo empirico para una cantidad grande de simbolos
static void test_largo_codigo();

static void test_esperanza();

// testea que el vector lambda sea correcto para varios valores de p distintos
static void test_vector_perm();

// testea que funcionan correctamente la codificacion y decodificacion
static void test_codigo_archivo();

};

#endif
