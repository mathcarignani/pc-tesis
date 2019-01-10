#ifndef __CODIGO_GOLOMB_BN_H__
#define __CODIGO_GOLOMB_BN_H__

#include "codigo.h"
#include "codigo_golomb.h"
#include "distribucion_bn.h"

class CodigoGolombBN : public Codigo {

private:
  CodigoGolomb* codigo_golomb;
  DistribucionBN* distribucion_bn;
  double p; 
  int lambda; // lambda depende de p
  std::vector <unsigned int> vector_perm; // tiene largo lambda
  std::vector <unsigned int> vector_perm_inverso; // tiene largo lambda
  double esperanza;

public:
  CodigoGolomb* get_codigo_golomb();
  double get_p();
  int get_l();
  int get_lambda();
  std::vector <unsigned int> get_vector_perm();
  std::vector <unsigned int> get_vector_perm_inverso();
  double get_esperanza();
  
  // calcula la esperanza practica teniendo en cuenta unicamente
  // los simbolos en el rango [simbolo_inicial,simbolo_final]
  double calcular_esperanza_practica(int simbolo_inicial, int simbolo_final);

  int calcular_k();

  CodigoGolombBN(int l, double p);

// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //

  // imprime la informacion que define al codigo en pantalla
  void mostrar_codigo();// = 0;  

  // Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
  // [3] para un codigo de golomb mod tiene en cuenta una distribucion binomial negativa
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
