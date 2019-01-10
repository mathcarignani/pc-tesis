#ifndef __DISTRIBUCION_GEO_H__
#define __DISTRIBUCION_GEO_H__

#include "distribucion.h"

class DistribucionGeo : public Distribucion {

public:
  
  double get_p();

  DistribucionGeo(double p_);
  
  // DISTRIBUCION GEOMETRICA ==> P(i)=(1-p)*(p**i)
  double prob(int i);

  // ENTROPIA (ANALITICA) DE LA DISTRIBUCION GEOMETRICA
  // ==> H(X)= h(p) / (1-p), donde h(p)= -p*log2(p) -(1-p)*log2(1-p)
  double entropia_analitica();

  // ESPERANZA (ANALITICA) DE LA DISTRIBUCION GEOMETRICA
  // ==> E(X)=p/(1-p)
  double esperanza_analitica();

  bool es_BN();
  
};

#endif
