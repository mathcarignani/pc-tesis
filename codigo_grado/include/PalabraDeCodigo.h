#ifndef __PALABRA_DE_CODIGO_H__
#define __PALABRA_DE_CODIGO_H__

#include <math.h>
#include <stdio.h>
#include <vector>
#include "Archivo.h"
#include "BitStream.h"
#include "impresion.h"

class PalabraDeCodigo {

private:
  unsigned int largo;
  std::vector <bool> entero;

  static void imprimir_unario(int n);

public:
  unsigned int get_largo();
  std::vector <bool> get_entero();

  /* CREADORES */
  PalabraDeCodigo(unsigned int largo);
  
  PalabraDeCodigo(unsigned int largo, std::vector <bool> entero);

  PalabraDeCodigo(unsigned int largo, unsigned int entero);

  /* OTROS PROCEDIMIENTOS */
  static PalabraDeCodigo* concatenar_unario(PalabraDeCodigo* palabra,
                                            int unario,
                                            bool antes);

  bool comparar_palabras(PalabraDeCodigo* palabra);

  void imprimir_palabra();

  void imprimir_palabra_espacios(int espacios_antes, int largo_total);

  static void imprimir_palabra_unario(PalabraDeCodigo* palabra,
                                      int unario,
                                      bool antes,
                                      int espacios_antes,
                                      int largo_total);

  void escribir_palabra_archivo(BitStreamWriter* archivo);
  
  static void escribir_palabra_unario_archivo(PalabraDeCodigo* palabra,
                                              int unario,
                                              bool antes,
                                              BitStreamWriter* archivo);

};

#endif
