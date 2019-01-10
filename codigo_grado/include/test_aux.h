#ifndef __TEST_AUX_H__
#define __TEST_AUX_H__

#include "Archivo.h"
#include "BitStream.h"
#include "clase_codigo_distribucion.h"
#include "codigo.h"
#include "distribucion.h"
#include "PalabraDeCodigo.h"

class TestAux {

public:

static std::vector <PalabraDeCodigo*> crear_codigo(int enteros[], int largos[], int cant_simbolos);

static double calcular_largo_medio_empirico(Codigo* codigo, Distribucion* distribucion);

// ####################################################################################################### //
// ################# auxiliares para testear codificadores / decodificadores con archivos ################ //
// ####################################################################################################### //

// genera un numero aleatorio entre min y max inclusive
static int generar_numero_aleatorio(int min, int max);

// crea un archivo donde los simbolos estan codificados con el codigo T
static void crear_archivo_codificado(Codigo* codigo,
                                     std::vector <int> & vector_chequeo,
                                     int maximo,
                                     int cant_repeticiones);

// decodifico el archivo creado en el procedimiento anterior y 
//   voy chequeando su correctitud para cada simbolo
// devuelve true sii todos los simbolos fueron decodificados correctamente
static bool decodificar_archivo(Codigo* codigo,
                                std::vector <int> vector_chequeo,
                                int cant_repeticiones);

};

#endif
