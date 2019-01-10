#include "codigo.h"
using namespace std;

// Esta funcion genera una estructura con informacion que carateriza el perfil del codigo 
//  (teniendo en cuenta secuencias y patrones que siguen los largos de las palabras)
Perfil* Codigo::generar_perfil(int cant_simbolos) {

  // [1] Se crea un vector de series a partir de los largos de las palabras de codigo
  vector <Patron*> series;
  int cant_series=0;

  Patron* serie;
  int primer_simbolo=0;
  int cant_palabras_largo_actual=0;

  int largo_i;
  int largo_i_mas_uno;
  bool guardar_serie;

  for (int i=0; i<cant_simbolos; i++){

    cant_palabras_largo_actual++; // sumo una palabra de largo igual al actual
    
    // Se crea y guarda una serie en alguno de estos dos casos:
    // (1) si no existe una siguiente palabra de codigo
    // (2) si existe una siguiente palabra de codigo y tiene largo diferente a la actual
    
    guardar_serie=(i==cant_simbolos-1); // caso (1)
    
    largo_i=codificar_simbolo_largo(i);

    if (!guardar_serie){ // existe una siguiente palabra de codigo

      largo_i_mas_uno=codificar_simbolo_largo(i+1);
      guardar_serie=(largo_i_mas_uno!=largo_i); // caso (2)
    }

    if (guardar_serie){
      serie=new Patron(primer_simbolo,i,cant_palabras_largo_actual,largo_i);
      series.push_back(serie);
      cant_series++;

      // seteo parametros para la proxima serie
      cant_palabras_largo_actual=0;
      primer_simbolo=i+1;
    }
  } // end for


  // [2] Se crea un vector de patrones a partir de la informacion del vector de series
  vector <Patron*> patrones;
  int cant_patrones=0;

  Patron* patron;
  primer_simbolo=0;
  int cant_series_patron_actual=0;


  int indice_mayor_patron=0;
  int largo_mayor_patron=0;
  int largo_patron_actual;

  int palabras_serie_i;
  int palabras_serie_i_mas_uno;
  int ultimo_simbolo;
  bool guardar_patron;

  for (int i=0; i<cant_series; i++){

    cant_series_patron_actual++; // sumo una serie al patron actual

    // Se crea y guarda un patron en alguno de estos dos casos:
    // (1) si no existe una siguiente serie
    // (2) si existe una siguiente serie y ( no tiene la misma cantidad de palabras
    //                                       o
    //                                       sus palabras no tienen largo
    //                                       una unidad mayor que las palabras de la serie actual )   
    
    guardar_patron=(i==cant_series-1); // caso (1)

    palabras_serie_i=series[i]->get_cant_palabras_serie();
    largo_i=series[i]->get_ultimo_largo();

    if (!guardar_patron){ // existe una siguiente serie

      palabras_serie_i_mas_uno=series[i+1]->get_cant_palabras_serie();
      largo_i_mas_uno=series[i+1]->get_ultimo_largo();

      // caso (2)
      guardar_patron=(palabras_serie_i_mas_uno!=palabras_serie_i)||(largo_i_mas_uno!=(largo_i+1));
    }

    if (guardar_patron){

      ultimo_simbolo=series[i]->get_ultimo_simbolo();

      patron=new Patron(primer_simbolo,ultimo_simbolo,cant_series_patron_actual,palabras_serie_i,largo_i);
      patrones.push_back(patron);
      cant_patrones++;

      // si es el patron de mayor largo lo guardo
      largo_patron_actual=ultimo_simbolo-primer_simbolo+1;
      if ( largo_patron_actual > largo_mayor_patron){
        largo_mayor_patron=largo_patron_actual;
        indice_mayor_patron=cant_patrones-1;
      }

      // seteo parametros para el proximo patron
      cant_series_patron_actual=0;

      if (i!=cant_series-1)
        primer_simbolo=series[i+1]->get_primer_simbolo();
    }
  } // end for
  
  Perfil* perfil;
  perfil=new Perfil(series,cant_series,patrones,cant_patrones,indice_mayor_patron);

  return perfil;
}


double Codigo::calcular_largo_medio(vector <double> probabilidades,
                                    vector <PalabraDeCodigo*> codigo,
                                    int simbolo_inicial, int simbolo_final){
  double largo_medio=0;

  for(int i=simbolo_inicial; i<=simbolo_final; i++){
    largo_medio+=probabilidades[i]*codigo[i]->get_largo();
  }
  return largo_medio;
}


void Codigo::imprimir_columnas(){
  printf("-----------------------------------------------------------------\n");
  printf("||    i   ||    P(i)        ||  L(C)  ||  C(i)                   \n");
  printf("-----------------------------------------------------------------\n");
}


void Codigo::imprimir_probabilidad(int i, double prob){

  int largo_palabra=codificar_simbolo_largo(i);

  int cant_espacios1=6-Impresion::cantidad_cifras(i);
  int cant_espacios3=6-Impresion::cantidad_cifras(largo_palabra);

  printf("||"); Impresion::imprimir_espacios(cant_espacios1); printf("%d  ",i);

  printf("||  %.10f  ",prob);

  printf("||"); Impresion::imprimir_espacios(cant_espacios3); printf("%d  ",largo_palabra);

  int unario;
  bool antes;
  PalabraDeCodigo* palabra=codificar_simbolo(i,unario,antes);

  printf("||  "); PalabraDeCodigo::imprimir_palabra_unario(palabra,unario,antes,0,0);

  printf("\n");
}


void Codigo::codificar_simbolo_archivo(int simbolo, BitStreamWriter* archivo){

  PalabraDeCodigo* palabra;
  int unario=0; // dummy
  bool antes=true; // dummy

  // dependiendo del tipo de codigo la implementacion de esta funcion es diferente
  palabra=codificar_simbolo(simbolo,unario,antes);

  // escribo la palabra en el archivo
  PalabraDeCodigo::escribir_palabra_unario_archivo(palabra,unario,antes,archivo);
}
