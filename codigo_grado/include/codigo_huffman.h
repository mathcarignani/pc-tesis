#ifndef __CODIGO_HUFFMAN_H__
#define __CODIGO_HUFFMAN_H__

#include "ArbolCodigo.h"
#include "clase_codigo_distribucion.h"
#include "codigo.h"
#include "distribucion.h"

class CodigoHuffman : public Codigo {

private:

  int cantidad_simbolos;
  ArbolCodigo* arbol_codigo;
  std::vector <PalabraDeCodigo*> vector_codigo;
  
  // opcion 1 - se crea el codigo a partir de un vector de probabilidades
  //             (cuyo largo es mayor o igual a cantidad_simbolos)
  std::vector <double> probabilidades;
  
  // opcion 2 - se crea el codigo a partir de una instancia de Distribucion
  Distribucion* distribucion;

  static void obtener_dos_probabilidades_menores(std::vector <Nodo*> huffman,
                                                 int cant_simbolos,
                                                 int & menor_indice_menor,
                                                 int & mayor_indice_menor);
  std::vector <Nodo*> crear_hojas();

  static ArbolCodigo* calcular_arbol(std::vector <Nodo*> huffman, int cant_simbolos);

  static std::vector <PalabraDeCodigo*> calcular_codigo_de_arbol(ArbolCodigo* arbol_codigo,
                                                                  int cant_simbolos,
                                                                  bool solo_largos);

  static void arbol_a_codigo(Nodo* nodo, int largo,
                             std::vector <bool> entero,
                             std::vector <PalabraDeCodigo*> & codigo);

  static void arbol_a_codigo_solo_largos(Nodo* nodo, int largo,
                                         std::vector <bool> entero,
                                         std::vector <PalabraDeCodigo*> & codigo);

public:

  int get_cantidad_simbolos();
  ArbolCodigo* get_arbol_codigo();
  std::vector <PalabraDeCodigo*> get_vector_codigo();
  std::vector <double> get_probabilidades();
  Distribucion* get_distribucion();

  // opcion 1 - se crea el codigo a partir de un vector de probabilidades
  //             (cuyo largo es mayor o igual a cantidad_simbolos)
  CodigoHuffman(int cant_simbolos,
                std::vector <double> probabilidades,
                bool solo_arbol,
                bool solo_largos);

  // opcion 2 - se crea el codigo a partir de una instancia de Distribucion
  CodigoHuffman(int cant_simbolos,
                Distribucion* distribucion,
                bool solo_arbol,
                bool solo_largos);

// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //

  // imprime la informacion que define al codigo en pantalla
  void mostrar_codigo();// = 0;  

  // Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
  // [1] para un codigo de huffman tiene en cuenta las probabilidades a partir de las cuales fue creado
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
