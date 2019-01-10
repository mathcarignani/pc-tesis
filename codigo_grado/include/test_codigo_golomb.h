#ifndef __TEST_CODIGO_GOLOMB_H__
#define __TEST_CODIGO_GOLOMB_H__

#include "codigo_golomb.h"
#include "distribucion_geo.h"
#include "test_aux.h"

class TestCodigoGolomb { 

private:

// ####################################################################################################### //
// ################## auxiliares de TestCodigoGolomb::test_codigo() ###################################### //
// ####################################################################################################### //

static bool comparar_codigos(std::vector <PalabraDeCodigo*> codigo_golomb_1,
                             CodigoGolomb* codigo_golomb_2,
                             int cant_simbolos);

static void test_golomb(int enteros[], int largos[], int l,
                        int cant_simbolos, int numero_test);

// ####################################################################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

static void test_largo_codigo_aux(int numero_test, double p);

static void test_codigo_archivo_aux(int numero_test, int l, int cant_repeticiones);

public:

// testea que funcionan correctamente la codificacion y decodificacion
static void test_codigo();

// testea que el largo de codigo calculado analiticamente
// es igual al largo de codigo empirico para una cantidad grande de simbolos
static void test_largo_codigo();

// testea que funcionan correctamente la codificacion y decodificacion
static void test_codigo_archivo();

};

#endif
