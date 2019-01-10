#ifndef __EXPERIMENTOS_H__
#define __EXPERIMENTOS_H__

#include "codigo_huffman.h"
#include "codigo_t.h"
#include "codigo_golomb.h"
#include "codigo_golomb_bn.h"
#include "distribucion_bn.h"
#include "distribucion_geo.h"
#include "impresion.h"
#include <time.h> 

class Experimentos {

private:
static void imprimir_columnas_codigo_golomb();
static void imprimir_columnas_codigo_huffman();
static void imprimir_columnas_codigo_t();
static void imprimir_columnas_golomb_bn();
static void actualizar_parametro_p(double & p, double & delta_p, int caso);

public:

// calcula los primeros n rangos de golomb
static void imprimir_rangos_golomb(int n);

// static void chequeo_codigo_golomb();

// codigo golomb
static void golomb();

// codigo_huffman
static void huffman();

// codigo_t
static void t();

// codigo_golomb_bn
static void golomb_bn();

};

#endif
