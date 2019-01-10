#ifndef __PERFIL_H__
#define __PERFIL_H__

#include <stdio.h>
#include <vector>
#include "impresion.h"

class Patron {

private:
  int primer_simbolo; // indice del primer simbolo de la primera serie del patron
  int ultimo_simbolo; // indice del ultimo simbolo de la ultima serie del patron
  int nro_de_series;       // numero de series sucesivas del patron, donde cada serie tiene la misma
  int cant_palabras_serie; //   cantidad 'cant_palabras_serie' de palabras de igual largo, y en cada serie
                           //   las palabras tienen largo una unidad mayor que el de las palabras de la
                           //   serie anterior
  int ultimo_largo; // largo que tienen las 'cant_palabras_serie' de la ultima serie del patron

public:
  int get_primer_simbolo();
  int get_ultimo_simbolo();
  int get_nro_de_series();
  int get_cant_palabras_serie();
  int get_ultimo_largo();

  /* crear patron */
  Patron(int primer_simbolo, int ultimo_simbolo, int nro_de_series, 
          int cant_palabras_serie, int ultimo_largo);

  /* crear serie */
  Patron(int primer_simbolo, int ultimo_simbolo,
       int cant_palabras_serie, int ultimo_largo);

  void imprimir_info_serie();

  void imprimir_info_patron();

  void imprimir_patron();

};  

class Perfil {

private:
  std::vector <Patron*> series;
  int cant_series;
  std::vector <Patron*> patrones;
  int cant_patrones;
  int indice_mayor_patron; // patrones[indice_mayor_patron] es el patron mas largo del perfil

public:
  std::vector <Patron*> get_series();
  int get_cant_series();
  std::vector <Patron*> get_patrones();
  int get_cant_patrones();
  int get_indice_mayor_patron();

  Perfil(std::vector <Patron*> series,  int cant_series,
       std::vector <Patron*> patrones, int cant_patrones,
       int indice_mayor_patron);  

  void imprimir_perfil();
};

#endif
