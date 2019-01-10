#include "clase_codigo_distribucion.h"
using namespace std;

ClaseCodigoDistribucion::ClaseCodigoDistribucion(Codigo* codigo_, Distribucion* distribucion_){
  codigo=codigo_;
  distribucion=distribucion_;
}

// ####################################################################################################### //
// ########################## ClaseCodigoDistribucion::calcular_largo_medio ############################## //
// ####################################################################################################### //

// calcula el largo medio del codigo teniendo en cuenta unicamente 
// los simbolos en el rango [simbolo_inicial,simbolo_final]
double ClaseCodigoDistribucion::calcular_largo_medio(int simbolo_inicial,
                                                      int simbolo_final){
  double largo_medio=0;

  for(int i=simbolo_inicial; i<=simbolo_final; i++){

    //printf("prob %.6f largo %d\n",distribucion->prob(i),codigo->codificar_simbolo_largo(i));
    
    largo_medio+=distribucion->prob(i)*codigo->codificar_simbolo_largo(i);
  }
  return largo_medio;
}

// ####################################################################################################### //
// ########################## ClaseCodigoDistribucion::imprimir_simbolos ################################# //
// ####################################################################################################### //

void ClaseCodigoDistribucion::imprimir_simbolos(int cant_simbolos, 
                                                bool imprimir_probs, bool imprimir_perfil_){
  if (imprimir_perfil_){
    Perfil* perfil;
    perfil=codigo->generar_perfil(cant_simbolos);

    if (imprimir_probs){
      imprimir_vector_probabilidades_y_perfil(cant_simbolos,perfil);
    }
    else{
      perfil->imprimir_perfil();
    }
  }
  else if (imprimir_probs){
    imprimir_vector_probabilidades(cant_simbolos);
  }
  printf("\n");
}

void ClaseCodigoDistribucion::imprimir_vector_probabilidades_y_perfil(int cant_simbolos,
                                                                       Perfil* perfil){
  Codigo::imprimir_columnas();
  
  vector <Patron*> series=perfil->get_series();
  vector <Patron*> patrones=perfil->get_patrones();

  Patron* serie;
  Patron* patron;
  int indice_serie=0;
  int indice_patron=0;
  
  // obtengo la primer serie y el primer patron
  serie=series[indice_serie];
  patron=patrones[indice_patron];  
  
  for (int i=0; i<cant_simbolos; i++){

    codigo->imprimir_probabilidad(i,distribucion->prob(i));

    // si termina una serie imprimo su informacion
    if (i==serie->get_ultimo_simbolo()){
      serie->imprimir_info_serie();

      if (i<cant_simbolos-1){ // quedan series porque quedan simbolos
        indice_serie++;
        serie=series[indice_serie];
      }

      // si termina un patron imprimo su informacion
      if (i==patron->get_ultimo_simbolo()){
        patron->imprimir_info_patron();

        if (i<cant_simbolos-1){ // quedan patrones porque quedan simbolos
          indice_patron++;
          patron=patrones[indice_patron];
        }
      }
    }
  } // end for
}

void ClaseCodigoDistribucion::imprimir_vector_probabilidades(int cant_simbolos){
  Codigo::imprimir_columnas();
    
  for (int i=0; i<cant_simbolos; i++){
    codigo->imprimir_probabilidad(i,distribucion->prob(i));
  } 
}
