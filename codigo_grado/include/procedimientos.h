#ifndef __PROCEDIMIENTOS_H__
#define __PROCEDIMIENTOS_H__

#include <vector>
#include "clase_codigo_distribucion.h"
#include "codigo_golomb.h"
#include "codigo_golomb_bn.h"
#include "codigo_huffman.h"
#include "codigo_t.h"
#include "distribucion_bn.h"
#include "distribucion_geo.h"

class Procedimientos {

public:

static void  mostrar_codigo_golomb(int l, double p);
static void imprimir_codigo_golomb(int l, double p_,
                                   int cant_simbolos, bool BN, double p,
                                   bool imprimir_probs, bool imprimir_perfil);

static void  mostrar_codigo_golomb_bn(int l, double p);
static void imprimir_codigo_golomb_bn(int l, double p_,
                                       int cant_simbolos, bool BN, double p,
                                       bool imprimir_probs, bool imprimir_perfil);

static void  mostrar_codigo_huffman(bool BN, double p, int cant_simbolos);
static void imprimir_codigo_huffman(bool BN_, double p_, int cant_simbolos_,
                                    int cant_simbolos, bool BN, double p,
                                    bool imprimir_probs, bool imprimir_perfil);

static void  mostrar_codigo_t(double p, int alfa, int beta);
static void imprimir_codigo_t(double p_, int alfa, int beta,
                                  int cant_simbolos, bool BN, double p,
                                  bool imprimir_probs, bool imprimir_perfil);
};

#endif


// ####################################################################################################### //
// ######################################## auxiliares ################################################### //
// ####################################################################################################### //

/*int imprimir_codigo_inicio(int tipo_codigo,bool BN,
                           double p,
                           int cant_simbolos,
                           std::vector <double> & probabilidades,
                           double & entropia_practica,
                           bool imprimir);

void imprimir_codigo_fin(int tipo_codigo,
                         bool BN,
                          double p,
                          std::vector <double> probabilidades,
                         std::vector <PalabraDeCodigo> codigo,
                         int cant_simbolos, 
                         bool imprimir_probabilidades,
                         bool imprimir_perfil,
                         int cant_simbolos_imprimir,
                         double largo_medio_analitico,
                         double entropia_practica,
                         int alfa,
                         int beta);


// ####################################################################################################### //
// ################################## imprimir_codigo_huffman ############################################ //
// ####################################################################################################### //

void imprimir_codigo_huffman(bool BN,
                             double p,
                             int cant_simbolos, 
                             bool imprimir_probabilidades,
                             bool imprimir_perfil,
                             int cant_simbolos_imprimir);


// ####################################################################################################### //
// ##################################### imprimir_codigo_golomb ########################################## //
// ####################################################################################################### //

void imprimir_codigo_golomb(bool BN,
                            double p,
                            int l, // TODO l = f(p,binomial_negativa)
                            int cant_simbolos, 
                            bool imprimir_probabilidades,
                            bool imprimir_perfil,
                            int cant_simbolos_imprimir);


// ####################################################################################################### //
// ################################# imprimir_codigo_t ############################################### //
// ####################################################################################################### //

void imprimir_codigo_t(double p,
                           int alfa, // TODO alfa = f(p)
                           int beta, // TODO beta = f(p)
                           int cant_simbolos, 
                           bool imprimir_probabilidades,
                           bool imprimir_perfil,
                           int cant_simbolos_imprimir);

// ####################################################################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

void calcular_esperanzas_distribuciones(double p, int n);

*/
