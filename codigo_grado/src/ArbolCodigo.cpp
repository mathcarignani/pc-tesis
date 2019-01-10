#include "ArbolCodigo.h"
using namespace std;

// ####################################################################################################### //
// ############################################# Nodo #################################################### //
// ####################################################################################################### //

int Nodo::get_entero(){
  return entero;
}
double Nodo::get_prob(){
  return prob;
}
void Nodo::set_prob(double prob_){
  prob=prob_;
}
Nodo* Nodo::get_hijo_cero(){
  return hijo_cero;
}
Nodo* Nodo::get_hijo_uno(){
  return hijo_uno;
}

/* CREADORES */
Nodo::Nodo(int ent, double pro){
  entero=ent;
  prob=pro;
  hijo_cero=NULL;
  hijo_uno=NULL;
}

Nodo::Nodo(Nodo * hijo_c, Nodo * hijo_u){
  entero=0; // no importa
  prob=hijo_c->get_prob() + hijo_u->get_prob();
  hijo_cero=hijo_c;
  hijo_uno=hijo_u;
}

/* OTROS PROCEDIMIENTOS */
bool Nodo::nodo_es_hoja(){
  bool res;
  res=(hijo_cero==NULL && hijo_uno==NULL);
  return res;
}

bool Nodo::nodo_es_igual(Nodo* otro_nodo){

  bool res=false;

  bool nodo_hoja=nodo_es_hoja();
  bool otro_nodo_hoja=otro_nodo->nodo_es_hoja();

  // si los dos nodos son hojas
  if ( nodo_hoja && otro_nodo_hoja ){
    // los nodos son iguales si tienen el mismo entero
    res=entero==(otro_nodo->get_entero());
  }
  // si ninguno de los dos nodos es hoja
  else if (!nodo_hoja && !otro_nodo_hoja){
    
    // los nodos son iguales si los respectivos hijos son iguales
    res=hijo_cero->nodo_es_igual(otro_nodo->get_hijo_cero());
    res= res && hijo_uno->nodo_es_igual(otro_nodo->get_hijo_uno());
  }

  return res;
}

// ####################################################################################################### //
// ######################################### ArbolCodigo ################################################ //
// ####################################################################################################### //

Nodo* ArbolCodigo::get_raiz(){
  return raiz;
}

ArbolCodigo::ArbolCodigo(Nodo* raiz_){
  raiz=raiz_;
}

bool ArbolCodigo::arbol_es_igual(ArbolCodigo* otro_arbol){
  bool res;
  res=raiz->nodo_es_igual(otro_arbol->get_raiz());
  return res;
}
