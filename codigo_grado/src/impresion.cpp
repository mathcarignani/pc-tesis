#include "impresion.h"
using namespace std;

int Impresion::cantidad_cifras(double numero){

  int cifras=1;
  int potencia_diez=10; // 10**cifras

  while (numero>=potencia_diez){
    cifras++;
    potencia_diez*=10;
  }
  return cifras;
}

void Impresion::imprimir_espacios(int cant){
  if (cant>0){
    for (int i=0; i<cant; i++)
      printf(" ");
  }  
}

void Impresion::imprimir_int(int entero, int espacios_antes, int largo_total){
  
  imprimir_espacios(espacios_antes);
  
  printf("%d",entero);
  
  int espacios_despues=largo_total-cantidad_cifras(entero);
  imprimir_espacios(espacios_despues);
}

void Impresion::imprimir_double(double numero, int cantidad_decimales, int espacios_antes, int largo_total){

  imprimir_espacios(espacios_antes);
  
  printf("%.*f",cantidad_decimales,numero);

  int largo_double=cantidad_cifras(numero)+1+cantidad_decimales; // 1 por la coma
  int espacios_despues=largo_total-largo_double;
  imprimir_espacios(espacios_despues);
}