#ifndef __CODIGO_H__
#define __CODIGO_H__

#include <cstdio>
#include <cstdlib>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <vector>
#include "Archivo.h"
#include "cuentas_codigo.h"
#include "impresion.h"
#include "PalabraDeCodigo.h"
#include "Perfil.h"

class Codigo {

public:  
  
  // Esta funcion genera una estructura con informacion que carateriza el perfil del codigo 
  //  (teniendo en cuenta secuencias y patrones que siguen los largos de las palabras)
  Perfil* generar_perfil(int cant_simbolos);

  static double calcular_largo_medio(std::vector <double> probabilidades,
                                     std::vector <PalabraDeCodigo*> vector,
                                     int simbolo_inicial, int simbolo_final);

  static void imprimir_columnas();

  void imprimir_probabilidad(int i, double prob);

  void codificar_simbolo_archivo(int simbolo, BitStreamWriter* archivo);

// ####################################################################################################### //
// ######################################## virtual ###################################################### //
// ####################################################################################################### //

  // imprime la informacion que define al codigo en pantalla
  virtual void mostrar_codigo() = 0;

  // Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
  // [1] para un codigo de huffman tiene en cuenta las probabilidades a partir de las cuales fue creado
  // [2] para un codigo de golomb tiene en cuenta una distribucion geometrica
  // [3] para un codigo de golomb mod tiene en cuenta una distribucion binomial negativa
  // [4] para el codigo t tiene en cuenta una distribucion binomial negativa
  virtual double largo_medio() = 0;

  // devuelve true sii los codigos son iguales (largo y palabra de codigo)
  virtual bool comparar_codigos(Codigo* codigo) = 0;

  // devuelve la palabra de codigo con la que se codifica un simbolo
  // si unario>=0 entonces se concatena el codigo unario 
  // si se concatena el codigo unario el booleano indica si va antes o despues
  virtual PalabraDeCodigo* codificar_simbolo(int simbolo, int & unario, bool & antes) = 0;

  // devuelve el largo de la palabra de codigo con que se codifica un simbolo
  virtual int codificar_simbolo_largo(int simbolo) = 0;

  // imprime en pantalla la palabra de codigo con la que se codifica un simbolo
  virtual void codificar_simbolo_imprimir(int simbolo, int espacios_antes, int largo_total) = 0;

  // decodifica el proximo simbolo leyendo del archivo
  // (devuelve -1 si termina el archivo antes)
  virtual int decodificar_simbolo_archivo(BitStreamReader* archivo) = 0;
  // Solamente lo implementan codigo_t y codigo_golomb_bn
  // (codigo_huffman tienen implementaciones dummy)
};

#endif
