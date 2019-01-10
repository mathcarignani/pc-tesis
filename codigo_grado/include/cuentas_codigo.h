#ifndef __CUENTAS_CODIGO_H__
#define __CUENTAS_CODIGO_H__

#include <cstdlib>
#include <iostream>
#include <math.h>
#include <stdio.h>

class CuentasCodigo {

public:  
  
  // Calcula la probabilidad del supersimbolo con indice gamma
  // P(gamma)= p(alfa+gamma) + p(alfa+gamma+beta) + p(alfa+gamma+2*beta) + .....
  //
  // PRECONDICIONES:
  // 0<p<1
  // alfa>=0
  // beta>=1
  // 0<=gamma<=beta-1
  static double calcular_probabilidad_supersimbolo(double p, int beta, int j);

  // [ver calculos en ecuacion TODO del informe]
  // llamado en CodigoGolombBN::largo_medio() y CodigoT::largo_medio() 
  static double calcular_largo_medio_supersimbolo(double p, int beta, int j, int largo_simbolo);

  // [ver calculos en paper Gallager-Van Voorhis]
  // llamado en CodigoGolomb::largo_medio()
  static double calcular_largo_medio_golomb_geometrica(double p, int l, int k, int acc);

};

#endif
