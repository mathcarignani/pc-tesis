#include "Perfil.h"
using namespace std;

// ####################################################################################################### //
// ############################################# Patron ################################################## //
// ####################################################################################################### //

int Patron::get_primer_simbolo(){
  return primer_simbolo;
}
int Patron::get_ultimo_simbolo(){
  return ultimo_simbolo;
}
int Patron::get_nro_de_series(){
  return nro_de_series;
}
int Patron::get_cant_palabras_serie(){
  return cant_palabras_serie;
}
int Patron::get_ultimo_largo(){
  return ultimo_largo;
}

/* crear patron */
Patron::Patron(int primer_simbolo_, int ultimo_simbolo_, int nro_de_series_, 
                 int cant_palabras_serie_, int ultimo_largo_){

  primer_simbolo=primer_simbolo_;
  ultimo_simbolo=ultimo_simbolo_;
  nro_de_series=nro_de_series_;
  cant_palabras_serie=cant_palabras_serie_;
  ultimo_largo=ultimo_largo_;
}

/* crear serie */
Patron::Patron(int primer_simbolo_, int ultimo_simbolo_, //int nro_de_series_, 
                 int cant_palabras_serie_, int ultimo_largo_){

  primer_simbolo=primer_simbolo_;
  ultimo_simbolo=ultimo_simbolo_;
  nro_de_series=1; // valor dummy, no tiene importancia
  cant_palabras_serie=cant_palabras_serie_;
  ultimo_largo=ultimo_largo_;
}

void Patron::imprimir_info_serie(){ 
  printf("----------------------------------------------------------------------\n");
  printf("|| fin serie [%d,%d] con ",primer_simbolo,ultimo_simbolo);

  if (cant_palabras_serie==1)
    printf("%d palabra de largo %d\n",cant_palabras_serie,ultimo_largo);
  else
    printf("%d palabras de largo %d\n",cant_palabras_serie,ultimo_largo);

  printf("----------------------------------------------------------------------\n");
}

void Patron::imprimir_info_patron(){
  printf("**********************************************************************\n");
  printf("|| fin patron [%d,%d] con ",primer_simbolo,ultimo_simbolo);

  if (nro_de_series==1){
    printf("%d serie de ",nro_de_series);

    if (cant_palabras_serie==1)
      printf("%d palabra de igual largo (%d)\n",cant_palabras_serie,ultimo_largo);
    else
      printf("%d palabras de igual largo (%d)\n",cant_palabras_serie,ultimo_largo);
  }  
  else {
    printf("%d series de ",nro_de_series);

    if (cant_palabras_serie==1)
      printf("%d palabra de igual largo\n",cant_palabras_serie);
    else
      printf("%d palabras de igual largo\n",cant_palabras_serie);
  }  
  printf("**********************************************************************\n");
}

void Patron::imprimir_patron(){
  int largo_rango=ultimo_simbolo-primer_simbolo+1;

  int cant_espacios1=9 - Impresion::cantidad_cifras(primer_simbolo)-Impresion::cantidad_cifras(ultimo_simbolo);
  int cant_espacios2=11 - Impresion::cantidad_cifras(largo_rango);
  int cant_espacios3=7 - Impresion::cantidad_cifras(nro_de_series);
  int cant_espacios4=9 - Impresion::cantidad_cifras(cant_palabras_serie);

  printf("||  [%d,%d]",primer_simbolo,ultimo_simbolo); Impresion::imprimir_espacios(cant_espacios1);

  printf("||   %d",largo_rango); Impresion::imprimir_espacios(cant_espacios2);

  if (nro_de_series==1){
    printf("||  %d",nro_de_series); Impresion::imprimir_espacios(cant_espacios3);
    printf("||  %d",cant_palabras_serie); Impresion::imprimir_espacios(cant_espacios4);
    printf("||  %d",ultimo_largo);

  }
  else {
    printf("||> %d",nro_de_series); Impresion::imprimir_espacios(cant_espacios3);
    printf("||> %d",cant_palabras_serie); Impresion::imprimir_espacios(cant_espacios4);

    int primer_largo=ultimo_largo-nro_de_series+1;
    int ultimo_simbolo_primera_serie=primer_simbolo+cant_palabras_serie-1;
    int primer_simbolo_ultima_serie=ultimo_simbolo-cant_palabras_serie+1;

    // rango y largo de palabras de la primera serie
    printf("||  %d[%d,%d] -- ",primer_largo,primer_simbolo,ultimo_simbolo_primera_serie);
    // rango y largo de palabras de la ultima serie
    printf("%d[%d,%d]",ultimo_largo,primer_simbolo_ultima_serie,ultimo_simbolo);
  }

  printf("\n");
}

// ####################################################################################################### //
// ############################################# Perfil ################################################## //
// ####################################################################################################### //

vector <Patron*> Perfil::get_series(){
  return series;
}
int Perfil::get_cant_series(){
  return cant_series;
}
vector <Patron*> Perfil::get_patrones(){
  return patrones;
}
int Perfil::get_cant_patrones(){
  return cant_patrones;
}
int Perfil::get_indice_mayor_patron(){
  return indice_mayor_patron;
}

Perfil::Perfil(vector <Patron*> series_,  int cant_series_,
                vector <Patron*> patrones_, int cant_patrones_,
               int indice_mayor_patron_){
  series=series_;
  cant_series=cant_series_;
  patrones=patrones_;
  cant_patrones=cant_patrones_;
  indice_mayor_patron=indice_mayor_patron_;
}

void Perfil::imprimir_perfil(){
  
  printf("------------------------------------------------------------------------------------\n");
  printf("||  rango i     || largo rango  || #series || #palabras ||  largo palabras          \n");
  printf("------------------------------------------------------------------------------------\n");

  Patron* patron;

  for (int i=0; i<cant_patrones; i++){
    patron=patrones[i];
    patron->imprimir_patron();
  }

}
