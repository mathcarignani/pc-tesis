#ifndef __CODIGO_GOLOMB_H__
#define __CODIGO_GOLOMB_H__

#include "ArbolCodigo.h"
#include "codigo.h"

class CodigoGolomb : public Codigo {

private:
  bool gpo2;
  int k; // solo importa cuando gpo2=true, l=2**k
  int l; // es igual al largo de vector_codigo
  double p; // solo importa cuando se pasa l=0, en caso contrario vale -1
  ArbolCodigo* arbol_codigo;
  std::vector <PalabraDeCodigo*> vector_codigo;

  static void calcular_k_y_acc(int l, int &k, int &acc);

  static Nodo* crear_arbol_golomb(int hojas, int largo, std::vector <bool> entero,
                                   std::vector <PalabraDeCodigo*> & codigo, int & indice_codigo);

public:
  int get_l();
  double get_p();
  ArbolCodigo* get_arbol_codigo();
  std::vector <PalabraDeCodigo*> get_vector_codigo();

  static int calcular_l(double p);

  static void calcular_rango_p(int l, double p, double &p_inf, double &p_sup);

  CodigoGolomb(int l, double p, bool gpo2, int k);

  // auxiliar de CodigoGolomb::mostrar_codigo()
  // tambien utilizado en CodigoGolombBN::mostrar_codigo()
  void mostrar_aux();

  // wrapper para distinguir casos cuando gpo2 es true y false
  PalabraDeCodigo* obtener_palabra(int i);

// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //

  // imprime la informacion que define al codigo en pantalla
  void mostrar_codigo();// = 0;  

  // Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
  // [2] para un codigo de golomb tiene en cuenta una distribucion geometrica
  double largo_medio();// = 0;

  // devuelve true sii los codigos son iguales (largo y palabra de codigo)
  bool comparar_codigos(Codigo* codigo);// = 0;

  // devuelve la palabra de codigo con la que se codifica un simbolo
  // si unario>=0 entonces se concatena el codigo unario 
  // si se concatena el codigo unario el booleano indica si va antes o despues
  PalabraDeCodigo* codificar_simbolo(int simbolo, int & unario, bool & antes);// = 0;

  // devuelve el largo de la palabra de codigo con que se codifica un simbolo
  int codificar_simbolo_largo(int simbolo);// = 0;

  // imprime en pantalla la palabra de codigo con la que se codifica un simbolo
  void codificar_simbolo_imprimir(int simbolo, int espacios_antes, int largo_total);// = 0;

  // decodifica el proximo simbolo leyendo del archivo
  // (devuelve -1 si termina el archivo antes)
  int decodificar_simbolo_archivo(BitStreamReader* archivo);// = 0;

};

#endif
