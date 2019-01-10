#ifndef __ARCHIVO_H__
#define __ARCHIVO_H__

#include <cstdio>
#include <cstdlib>
#include <string>
#include "BitStream.h"

class Archivo {

public:

  // Compara dos archivos, retornando 0 si son iguales
  // y el numero del primer bit diferente si son distintos
  static int comparar_dos_archivos(char* file1, char* file2);

  // codifica el entero n en unario en el archivo asociado al stream de entrada
  static void codificar_unario(BitStreamWriter* archivo, int n);

  // decodifica el proximo unario, devolviendo -1 si termina el archivo antes
  static int decodificar_unario(BitStreamReader* archivo);

};

#endif

/*
// Crea el archivo "file_name" de tamano "bytes_size" bytes
// donde cada bit se elige siguiendo una distribucion Bernoulli~(prob_succ)
// con 0<prob_succ<1 y p(1)=prob_succ y p(0)=1-prob_succ
void crear_archivo_bernoulli(char* output_file_name, double prob_succ, int bytes_size);

// Lee el archivo "input_file_name" y cuenta ceros y unos
void leer_archivo_bernoulli(char* input_file_name);

// Suma bit a bit dos archivos del mismo largo (0+0=0, 0+1=1+0=1, 1+1=1)
void sumar_dos_archivos(char* file1, char* file2, char* output_file_name);
*/

