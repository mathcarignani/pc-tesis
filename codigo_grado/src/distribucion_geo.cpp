#include "distribucion_geo.h"
using namespace std;

double DistribucionGeo::get_p(){
  return p;
}

DistribucionGeo::DistribucionGeo(double p_){
  p=p_;
}

// DISTRIBUCION GEOMETRICA ==> P(i)=(1-p)*(p**i)
double DistribucionGeo::prob(int i){
  double res;
  res=(1-p)*pow(p,i);
  return res;
}

// ENTROPIA (ANALITICA) DE LA DISTRIBUCION GEOMETRICA
// ==> H(X)= h(p) / (1-p), donde h(p)= -p*log2(p) -(1-p)*log2(1-p)
double DistribucionGeo::entropia_analitica(){
  double ent;
  ent=( -p*( log(p)/log(2) ) - (1-p)*( log(1-p)/log(2) ) ) / (1-p);
  return ent;
}

// ESPERANZA (ANALITICA) DE LA DISTRIBUCION GEOMETRICA
// ==> E(X)=p/(1-p)
double DistribucionGeo::esperanza_analitica(){
  double esp;
  esp=p/(1-p);
  return esp;
}

bool DistribucionGeo::es_BN(){
  return false;
}
