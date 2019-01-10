#ifndef __IMPRESION_H__
#define __IMPRESION_H__

#include <math.h>
#include <stdio.h>
#include <vector>

class Impresion {

public:

  // devuelve la cantidad de cifras que tiene un numero a la izquierda de la coma
  static int cantidad_cifras(double numero);

  // imprime cant espacios (si cant<=0 no imprime nada)
  static void imprimir_espacios(int cant);

  static void imprimir_int(int entero, int espacios_antes, int largo_total);

  static void imprimir_double(double numero, int cantidad_decimales, int espacios_antes, int largo_total);

};

#endif
