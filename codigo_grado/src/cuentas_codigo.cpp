#include "cuentas_codigo.h"
using namespace std;

// Calcula la probabilidad del supersimbolo con indice gamma
// P(gamma)= p(alfa+gamma) + p(alfa+gamma+beta) + p(alfa+gamma+2*beta) + .....
//
// PRECONDICIONES:
// 0<p<1
// alfa>=0
// beta>=1
// 0<=gamma<=beta-1
double CuentasCodigo::calcular_probabilidad_supersimbolo(double p, int beta, int j){
  
  if ( (p<=0) || (p>=1) || (beta<1) || (j<0) ) {
    printf("ERROR: calcular_probabilidad_supersimbolo\n");
    exit(1);
  }

  double res;
  double q_cuadrado=(1-p)*(1-p);
  double cociente=1-pow(p,beta);

  // antes de despejar
  // res=q_cuadrado*pow(p,alfa+gamma)*( (alfa+gamma+1)/cociente + (beta*pow(p,beta))/(cociente*cociente)  );

  //res=q_cuadrado*pow(p,alfa+gamma)*( ( (-alfa+beta-gamma-1)*pow(p,beta)+alfa+gamma+1 )/(cociente*cociente) );

  double primer_termino=(-j+beta-1)*pow(p,beta);
  
  double segundo_termino=j+1;

  res=q_cuadrado*pow(p,j)*(primer_termino+segundo_termino)/pow(cociente,2);

  return res;
}

// [ver calculos en ecuacion TODO del informe]
// llamado en CodigoGolombBN::largo_medio() y CodigoT::largo_medio() 
double CuentasCodigo::calcular_largo_medio_supersimbolo(double p, int beta, int j, int largo_simbolo){
  double res;
  double q_cuadrado=(1-p)*(1-p);
  double cociente=1-pow(p,beta);

  //double primer_termino=largo_simbolo*(alfa-beta+gamma+1)*pow(p,2*beta);
  //double segundo_termino=( -alfa+2*beta-gamma-1 + largo_simbolo*(-2*alfa+beta-2*gamma-2) )*pow(p,beta);
  //double tercer_termino=(largo_simbolo + 1)*(alfa+gamma+1);

  //res=q_cuadrado*pow(p,alfa+gamma)*(primer_termino+segundo_termino+tercer_termino)/(pow(cociente,3));

  double primer_termino=largo_simbolo*(j-beta+1)*pow(p,2*beta);

  double segundo_termino=(-j+2*beta-1+largo_simbolo*(-2*j+beta-2))*pow(p,beta);

  double tercer_termino=(largo_simbolo+1)*(j+1);

  res=q_cuadrado*pow(p,j)*(primer_termino+segundo_termino+tercer_termino)/(pow(cociente,3));

  return res;
}

// [ver calculos en paper Gallager-Van Voorhis]
// llamado en CodigoGolomb::largo_medio()
double CuentasCodigo::calcular_largo_medio_golomb_geometrica(double p, int l, int k, int acc){
  double res;
  // l es potencia de 2
  if (acc==l){
    res=k+1+pow(p,l)/(1-pow(p,l));
  }
  // l no es potencia de 2
  else {
    res=k+pow(p,acc-l)/(1-pow(p,l));
  }
  return res;
}
