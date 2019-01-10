#include "PalabraDeCodigo.h"
using namespace std;


// ####################################################################################################### //
// ########################################### privados ################################################## //
// ####################################################################################################### //

void PalabraDeCodigo::imprimir_unario(int n){
  for (int i=0; i<(int)n; i++)
    printf("0");
  printf("1");
}

// ####################################################################################################### //
// ########################################### publicos ################################################## //
// ####################################################################################################### //

unsigned int PalabraDeCodigo::get_largo(){
  return largo;
}
vector <bool> PalabraDeCodigo::get_entero(){
  return entero;
}

/* CREADORES */
PalabraDeCodigo::PalabraDeCodigo(unsigned int largo_){
  largo=largo_;
}

PalabraDeCodigo::PalabraDeCodigo(unsigned int largo_, vector <bool> entero_){
  largo=largo_;
  entero=entero_;
}

PalabraDeCodigo::PalabraDeCodigo(unsigned int largo_, unsigned int entero_){ 
  
  largo=largo_;

  int resto=entero_;
  int j=pow(2,largo);

  while (resto>=0){
    j/=2;
    if (resto>=j){
      entero.push_back(true);
      resto-=j;
    }
    else{
      entero.push_back(false);
    }

    if (j==1){
      resto=-1;
    }
  }
}

/* OTROS PROCEDIMIENTOS */
PalabraDeCodigo* PalabraDeCodigo::concatenar_unario(PalabraDeCodigo* palabra,
                                                     int unario,
                                                     bool antes){
  unsigned int largo_res=unario+1;
  vector <bool> entero_res;

  // agrego el unario
  // casos: unario y unario|palabra
  if ( palabra==NULL || (unario>=0 && antes) ){
    for(int i=0; i<unario; i++){
      entero_res.push_back(false);
    }
    entero_res.push_back(true);
  }

  // agrego la palabra
  // casos: palabra y palabra|unario
  if (palabra!=NULL){
    unsigned int largo_palabra=palabra->get_largo();
    vector <bool> entero_palabra=palabra->get_entero();

    for(int i=0; i<(int)largo_palabra; i++){
      entero_res.push_back(entero_palabra[i]);
    }
    largo_res+=largo_palabra;

    // caso palabra|unario
    if (unario>=0 && !antes){
      for(int i=0; i<unario; i++){
        entero_res.push_back(false);
      }
      entero_res.push_back(true);
    }
  } 

  PalabraDeCodigo* palabra_res=new PalabraDeCodigo(largo_res,entero_res);
  return palabra_res;
}

bool PalabraDeCodigo::comparar_palabras(PalabraDeCodigo* palabra){
  bool igual;
  igual=(largo==palabra->get_largo());
  if (igual){
    vector <bool> entero_palabra=palabra->get_entero();
    for(int i=0; i<(int)largo; i++){
      igual=(entero[i]==entero_palabra[i]);
      if (!igual){
        break;
      }
    }
  }
  return igual;
}

void PalabraDeCodigo::imprimir_palabra(){
  for(int i=0; i<(int)largo; i++){
    if (entero[i]){
      printf("1");
    }
    else {
      printf("0");
    }
  }
}

void PalabraDeCodigo::imprimir_palabra_espacios(int espacios_antes, int largo_total){
  Impresion::imprimir_espacios(espacios_antes);
  imprimir_palabra();
  Impresion::imprimir_espacios(largo_total-largo);
}

void PalabraDeCodigo::imprimir_palabra_unario(PalabraDeCodigo* palabra,
                                              int unario,
                                              bool antes,
                                              int espacios_antes,
                                              int largo_total){
  if (palabra==NULL){
    // unario
    if (unario!=-1){
      Impresion::imprimir_espacios(espacios_antes);
      imprimir_unario(unario);
      Impresion::imprimir_espacios(largo_total-(unario+1));
    }
  }
  else {
    // palabra
    if (unario==-1){
      palabra->imprimir_palabra_espacios(espacios_antes,largo_total);
    }
    else {
      Impresion::imprimir_espacios(espacios_antes);
      
      // unario|palabra
      if (antes){
        imprimir_unario(unario);
        palabra->imprimir_palabra();
      }
      // palabra|unario
      else {
        palabra->imprimir_palabra();
        imprimir_unario(unario);        
      }

      Impresion::imprimir_espacios(largo_total-(palabra->get_largo()+unario+1));
    }
  }
}


void PalabraDeCodigo::escribir_palabra_archivo(BitStreamWriter* archivo){
  for(int i=0; i<(int)largo; i++){
    if (entero[i]){
      archivo->pushBit(1);
    }
    else {
      archivo->pushBit(0);
    }
  }
}

void PalabraDeCodigo::escribir_palabra_unario_archivo(PalabraDeCodigo* palabra,
                                                      int unario,
                                                      bool antes,
                                                      BitStreamWriter* archivo){
  if (palabra==NULL){
    // unario
    if (unario!=-1){
      Archivo::codificar_unario(archivo,unario);
    }
  }
  else {
    // palabra
    if (unario==-1){
      palabra->escribir_palabra_archivo(archivo);
    }
    else {

      // unario|palabra
      if (antes){
        Archivo::codificar_unario(archivo,unario);
        palabra->escribir_palabra_archivo(archivo);
      }
      // palabra|unario
      else {
        palabra->escribir_palabra_archivo(archivo);
        Archivo::codificar_unario(archivo,unario);
      }
    }
  }

}
