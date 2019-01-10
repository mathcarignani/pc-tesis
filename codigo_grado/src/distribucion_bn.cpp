#include "distribucion_bn.h"
using namespace std;

double DistribucionBN::get_p(){
  return p;
}

DistribucionBN::DistribucionBN(double p_){
  p=p_;
}

bool DistribucionBN::es_BN(){
  return true;
}

// DISTRIBUCION BINOMIAL NEGATIVA ==> P(i)=(i+1)*((1-p)**2)*(p**i)
double DistribucionBN::prob(int i){
  double res;
  res=(i+1)*pow(1-p,2)*pow(p,i);
  return res;
}

// ENTROPIA (ANALITICA) DE LA DISTRIBUCION BINOMIAL NEGATIVA
// ==> H(X)= TODO
double DistribucionBN::entropia_analitica(){
  double ent;
  ent=0; // TODO
  return ent;
}

// ESPERANZA (ANALITICA) DE LA DISTRIBUCION BINOMIAL NEGATIVA
// ==> E(X)=2*p/(1-p)
double DistribucionBN::esperanza_analitica(){
  double esp;
  esp=2*p/(1-p);
  return esp;
}

// calcula el i donde se anula la derivada de la funcion de probabilidad de la distribucion BN
//   es decir que el entero que tiene mayor probabilidad es floor[i] o ceil[i] 
double DistribucionBN::calcular_i_prima(){
  double i_prima_=-(1+1/log(p));
  return i_prima_;
}

// calcula el minimo entero lambda_>0 tal que P(0)>=P(lambda)
int DistribucionBN::calcular_lambda(double i_prima_){

  int lambda_;

  // la funcion de probabilidad decrece en [0, inf)
  //   es decir P(0)>P(i) para todo i positivo, tomo lambda_=1
  if (i_prima_<=0){
    lambda_=1; // en este caso el vector lambda es lambda[0]=0
  }
  else {

    lambda_=(int)floor(i_prima_); // lambda_>=0 porque i_prima_>0
    if (lambda_==0)  lambda_++; // lambda>=1

    double prob_0=prob(0);
    double prob_i=prob(lambda_);

    while (prob_0<prob_i){
      lambda_++;
      prob_i = prob(lambda_);
    }
  }

  return lambda_;
}

// Este procedimiento se utiliza al codificar una BN con un codigo de golomb
//   ya que ordena los primeros simbolos (hasta que la probabilidad se vuelve decreciente)
//  por orden de probabilidad decreciente
// Devuelve vector_perm, i_prima y lambda
vector <unsigned int> DistribucionBN::calcular_vector_perm(double & i_prima, 
                                                              int & lambda){

  i_prima=calcular_i_prima();
  lambda=calcular_lambda(i_prima);
  vector <unsigned int> vector_perm(lambda,0);

  if (lambda==1){ // caso limite, P(0)>=P(i) para todo i>0
    vector_perm[0]=0;
  }
  else { // lambda>1, es decir que existe un i>0 tal que P(i)>P(0)
    // obtengo la mayor distribucion de probabilidad
    int min=(int) floor(i_prima);
    int max=(int) ceil(i_prima);

    if (min==max){ // si i_prima es un entero
      max++;
    }

    for (int i=0; i<lambda; i++){ // en cada iteracion agrego una probabilidad al vector
    
      // calculo las dos mayores probabilidades asociadas a indices
      // que todavia no fueron agregados al vector
      double min_prob=prob(min);
      double max_prob=prob(max);

      if (min_prob>max_prob){ // nota: si son iguales tomo el mayor indice max
        //printf("vector_perm[%d]=%d\n",min,i);
        vector_perm[min]=i;
        min--;
      }
      else{
        //printf("vector_perm[%d]=%d\n",max,i);
        vector_perm[max]=i;
        max++;
      }
    } // end for
  }

  return vector_perm;
}

vector <unsigned int> DistribucionBN::calcular_vector_perm_inverso(vector <unsigned int> vector_perm,
                                                                     int lambda){
  vector <unsigned int> vector_perm_inverso(lambda,0);

  for (int i=0; i<lambda; i++){
    vector_perm_inverso[vector_perm[i]]=i;
  }

  return vector_perm_inverso;
}

// calcula la esperanza analitica de [lambda,inf)
double DistribucionBN::esperanza_analitica_cola(int inicio){

  double primer_termino = inicio*(inicio-1)*pow(p,2);

  double segundo_termino = -2*(pow(inicio,2)-1)*p;

  double tercer_termino = inicio*(inicio+1);

  double res = (pow(p,inicio)/(1-p))*(primer_termino + segundo_termino + tercer_termino);

  //printf("\nesperanza analitica cola = %.5f\n",res);

  return res;
}

