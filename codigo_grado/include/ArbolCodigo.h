#ifndef __ARBOL_CODIGO_H__
#define __ARBOL_CODIGO_H__

#include <cstddef>

class Nodo {

private:
  int entero; // este atributo solo tiene sentido si el nodo es una hoja
  double prob; 
  Nodo* hijo_cero;
  Nodo* hijo_uno;

public:
  int get_entero();
  double get_prob();
  void set_prob(double prob);
  Nodo* get_hijo_cero();
  Nodo* get_hijo_uno();

  /* CREADORES */
  Nodo(int ent, double pro); // crea un nodo hoja
  Nodo(Nodo * hijo_c, Nodo * hijo_u); // crea un nodo que no es hoja

  /* OTROS PROCEDIMIENTOS */
  bool nodo_es_hoja();
  bool nodo_es_igual(Nodo* otro_nodo);

};

class ArbolCodigo {

private:  
  Nodo* raiz;

public:
  Nodo* get_raiz();

  ArbolCodigo(Nodo* raiz_);

  bool arbol_es_igual(ArbolCodigo* otro_arbol);

};

#endif
