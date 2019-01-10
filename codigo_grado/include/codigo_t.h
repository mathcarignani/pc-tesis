#ifndef __CODIGO_T_H__
#define __CODIGO_T_H__

#include "ArbolCodigo.h"
#include "codigo.h"
#include "codigo_golomb.h"
#include "codigo_huffman.h"
#include "distribucion_bn.h"

class CodigoT : public Codigo {

private:
  
  double p;
  int alfa;
  int beta;
  ArbolCodigo* arbol_codigo;
  std::vector <PalabraDeCodigo*> vector_codigo;
  std::vector <double> probabilidades_huffman;

  void calcular_alfa_y_beta();

  // Es similar al procedimiento generar_vector_probabilidades, las diferencias son que:
  //   >> en este caso solo interesa la distribucion binomial negativa
  //   >> no se realiza ningun chequeo de precision
  //   >> no se calcula la entropia empirica
  // PRE: se llamo antes al procedimiento generar_vector_probabilidades con cant_simbolos>alfa
  static std::vector <double> generar_vector_probabilidades_para_huffman(double p,
                                                                         int alfa,
                                                                         int beta);
public:
  int get_alfa();
  int get_beta();
  
  CodigoT(double p, int alfa, int beta);

// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //

  // imprime la informacion que define al codigo en pantalla
  void mostrar_codigo();// = 0;  

  // Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
  // [4] para el codigo t tiene en cuenta una distribucion binomial negativa
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
