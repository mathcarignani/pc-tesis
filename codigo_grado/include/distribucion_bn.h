#ifndef __DISTRIBUCION_BN_H__
#define __DISTRIBUCION_BN_H__

#include "distribucion.h"

class DistribucionBN : public Distribucion {

private:
  double i_prima;
  int lambda;

public:

  DistribucionBN(double p_);

  // calcula el i donde se anula la derivada de la funcion de probabilidad de la distribucion BN
  double calcular_i_prima();

  // calcula el minimo entero lambda>0 tal que P(0)>P(lambda), en el caso de la BN
  //   (a partir de este lambda la funcion de probabilidad es decreciente)
  int calcular_lambda(double i_prima);

  // Este procedimiento se utiliza al codificar una BN con un codigo de golomb
  //   ya que ordena los primeros simbolos (hasta que la probabilidad se vuelve decreciente)
  //  por orden de probabilidad decreciente
  // Devuelve vector_perm, i_prima y lambda
  std::vector <unsigned int> calcular_vector_perm(double & i_prima, 
                                                     int & lambda);

  std::vector <unsigned int> calcular_vector_perm_inverso(std::vector <unsigned int> vector_perm,
                                                            int lambda);

  // calcula la esperanza analitica de [inicio,inf)
  double esperanza_analitica_cola(int inicio);

// ####################################################################################################### //
// ######################################## distribucion.h ############################################### //
// ####################################################################################################### //

  double get_p();

  // DISTRIBUCION BINOMIAL NEGATIVA ==> P(i)=(i+1)*((1-p)**2)*(p**i)
  double prob(int i);
  
  // ENTROPIA (ANALITICA) DE LA DISTRIBUCION BINOMIAL NEGATIVA
  // ==> H(X)= TODO
  double entropia_analitica();

  // ESPERANZA (ANALITICA) DE LA DISTRIBUCION BINOMIAL NEGATIVA
  // ==> E(X)=2*p/(1-p)
  double esperanza_analitica();

  bool es_BN();

};

#endif
