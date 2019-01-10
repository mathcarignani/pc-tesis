#ifndef __CLASE_CODIGO_DISTRIBUCION_H__
#define __CLASE_CODIGO_DISTRIBUCION_H__

#include <cstdio>
#include <cstdlib>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <vector>
#include "codigo.h"
#include "distribucion.h"
#include "impresion.h"
#include "PalabraDeCodigo.h"
#include "Perfil.h"

class ClaseCodigoDistribucion {

private:
  Codigo* codigo;
  Distribucion* distribucion;

public:

  ClaseCodigoDistribucion(Codigo* codigo, Distribucion* distribucion);

  // calcula el largo medio empirico del codigo/distribucion teniendo en cuenta unicamente 
  // los simbolos en el rango [simbolo_inicial,simbolo_final]
  double calcular_largo_medio(int simbolo_inicial, int simbolo_final);

  void imprimir_simbolos(int cant_simbolos, bool imprimir_probs, bool imprimir_perfil);

  void imprimir_vector_probabilidades(int cant_simbolos);

  void imprimir_vector_probabilidades_y_perfil(int cant_simbolos,
                                                Perfil* perfil);
};

#endif
