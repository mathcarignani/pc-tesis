#ifndef __TEST_CODIGO_T_H__
#define __TEST_CODIGO_T_H__

#include "codigo_t.h"
#include "impresion.h"
#include "test_aux.h"

class TestCodigoT {

private: 

static void test_largo_codigo_aux(int numero_test, double p);

static void test_codigo_archivo_aux(int numero_test, double p, int cant_repeticiones);

public:

// testea que el largo de codigo calculado analiticamente
// es igual al largo de codigo empirico para una cantidad grande de simbolos
static void test_largo_codigo();

// testea que funcionan correctamente la codificacion y decodificacion
static void test_codigo_archivo();

};

#endif
