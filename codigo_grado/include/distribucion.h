#ifndef __DISTRIBUCION_H__
#define __DISTRIBUCION_H__

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

// precision con la que se hacen los calculos en generar_vector
#define precision_ 0.0000000001

class Distribucion {

protected:

  double p;

private: 

  // Calcula un termino de la entropia empirica.
  static double termino_entropia_practica(double prob);

  // Devuelve false si falla la precision (en ese caso se va acumular en el simbolo i_actual)
  bool chequeo_precision(int i_anterior, int i_actual);

  // Devuelve el minimo entero i tal que chequeo_precision(i-1,i,p)=false
  // (es decir que i es el indice del entero en el que se acumula)
  int calcular_largo_vector(int entero_acc);

public:  

  // genera el vector de probabilidades de largo cant_simbolos
  std::vector <double> generar_vector(int & cant_simbolos, double & entropia_practica);

  // analogo a Distribucion::generar_vector pero sin el vector
  double calcular_entropia_practica(int & cant_simbolos);

// ####################################################################################################### //
// ######################################## virtual ###################################################### //
// ####################################################################################################### //

  virtual double get_p() = 0;

  // devuelve la probabilidad del entero i
  virtual double prob(int i) = 0;

  virtual double entropia_analitica() = 0;

  virtual double esperanza_analitica() = 0;

  virtual bool es_BN() = 0;
  
};

#endif
