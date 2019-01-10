#include "procedimientos.h"
using namespace std;

// ####################################################################################################### //
// ##################################### mostrar codigos ################################################# //
// ####################################################################################################### //

void Procedimientos::mostrar_codigo_golomb(int l, double p_){
  CodigoGolomb* codigo_golomb;
  codigo_golomb=new CodigoGolomb(l,p_,false,-1);
  codigo_golomb->mostrar_codigo();
}

void Procedimientos::imprimir_codigo_golomb(int l, double p_,
                                            int cant_simbolos, bool BN, double p,
                                            bool imprimir_probs, bool imprimir_perfil){
  // creo el codigo
  CodigoGolomb* codigo_golomb;
  codigo_golomb=new CodigoGolomb(l,p_,false,-1);

  // creo la distribucion
  Distribucion* distribucion;
  distribucion=(BN)? ((Distribucion*)new DistribucionBN(p)) : ((Distribucion*)new DistribucionGeo(p));
  
  // creo el codigo-distribucion
  ClaseCodigoDistribucion* codigo_distribucion;
  codigo_distribucion=new ClaseCodigoDistribucion(codigo_golomb,distribucion);

  codigo_distribucion->imprimir_simbolos(cant_simbolos,imprimir_probs,imprimir_perfil);
}


void Procedimientos::mostrar_codigo_golomb_bn(int l, double p_){
  CodigoGolombBN* codigo_golomb_bn;
  codigo_golomb_bn=new CodigoGolombBN(l,p_);
  codigo_golomb_bn->mostrar_codigo();
}

void Procedimientos::imprimir_codigo_golomb_bn(int l, double p_,
                                                int cant_simbolos, bool BN, double p,
                                                bool imprimir_probs, bool imprimir_perfil){
  // creo el codigo
  CodigoGolombBN* codigo_golomb_bn;
  codigo_golomb_bn=new CodigoGolombBN(l,p_);

  // creo la distribucion
  Distribucion* distribucion;
  distribucion=(BN)? ((Distribucion*)new DistribucionBN(p)) : ((Distribucion*)new DistribucionGeo(p));
  
  // creo el codigo-distribucion
  ClaseCodigoDistribucion* codigo_distribucion;
  codigo_distribucion=new ClaseCodigoDistribucion(codigo_golomb_bn,distribucion);

  codigo_distribucion->imprimir_simbolos(cant_simbolos,imprimir_probs,imprimir_perfil);
}


void Procedimientos::mostrar_codigo_huffman(bool BN_, double p_, int cant_simbolos_){
  // creo la distribucion para el codigo
  Distribucion* distribucion;
  distribucion=(BN_)? ((Distribucion*)new DistribucionBN(p_)) : ((Distribucion*)new DistribucionGeo(p_));

  // creo el codigo a partir de la distribucion
  CodigoHuffman* codigo_huffman;
  codigo_huffman=new CodigoHuffman(cant_simbolos_,distribucion,false,false);
  codigo_huffman->mostrar_codigo();
}

void Procedimientos::imprimir_codigo_huffman(bool BN_, double p_, int cant_simbolos_,
                                              int cant_simbolos, bool BN, double p,
                                              bool imprimir_probs, bool imprimir_perfil){
  // creo la distribucion para el codigo
  Distribucion* distribucion_;
  distribucion_=(BN_)? ((Distribucion*)new DistribucionBN(p_)) : ((Distribucion*)new DistribucionGeo(p_));

  // creo el codigo a partir de la distribucion
  CodigoHuffman* codigo_huffman;
  codigo_huffman=new CodigoHuffman(cant_simbolos_,distribucion_,false,false);

  // creo la distribucion
  Distribucion* distribucion;
  distribucion=(BN)? ((Distribucion*)new DistribucionBN(p)) : ((Distribucion*)new DistribucionGeo(p));
  
  // creo el codigo-distribucion
  ClaseCodigoDistribucion* codigo_distribucion;
  codigo_distribucion=new ClaseCodigoDistribucion(codigo_huffman,distribucion);

  codigo_distribucion->imprimir_simbolos(cant_simbolos,imprimir_probs,imprimir_perfil);
}


void Procedimientos::mostrar_codigo_t(double p_, int alfa, int beta){
  CodigoT* codigo_t;
  codigo_t=new CodigoT(p_,alfa,beta);
  codigo_t->mostrar_codigo();
}

void Procedimientos::imprimir_codigo_t(double p_, int alfa, int beta,
                                            int cant_simbolos, bool BN, double p,
                                            bool imprimir_probs, bool imprimir_perfil){
  // creo el codigo
  CodigoT* codigo_t;
  codigo_t=new CodigoT(p_,alfa,beta);

  // creo la distribucion
  Distribucion* distribucion;
  distribucion=(BN)? ((Distribucion*)new DistribucionBN(p)) : ((Distribucion*)new DistribucionGeo(p));
  
  // creo el codigo-distribucion
  ClaseCodigoDistribucion* codigo_distribucion;
  codigo_distribucion=new ClaseCodigoDistribucion(codigo_t,distribucion);

  codigo_distribucion->imprimir_simbolos(cant_simbolos,imprimir_probs,imprimir_perfil);
}
