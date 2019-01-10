#include "Archivo.h"
using namespace std;

// Compara dos archivos, retornando 0 si son iguales
// y el numero del primer bit diferente si son distintos
int Archivo::comparar_dos_archivos(char* file1, char* file2){

  BitStreamReader* reader1=new BitStreamReader(file1);
  BitStreamReader* reader2=new BitStreamReader(file2);

  int cont=1; // primer bit diferente entre los archivos

  while (!reader1->reachedEOF()){
    if (reader2->reachedEOF()) return cont;
    if (reader1->getBit()!=reader2->getBit()) return cont;
    cont++;
  }
  if (!reader2->reachedEOF()) return cont;
  
  return 0;
}

// codifica el entero n en unario en el archivo asociado al stream de entrada
void Archivo::codificar_unario(BitStreamWriter* archivo, int n){
  for (int i=0; i<n; i++)
    archivo->pushBit(0);
  archivo->pushBit(1);
}

// decodifica el proximo unario, devolviendo -1 si termina el archivo antes
int Archivo::decodificar_unario(BitStreamReader* archivo){

  int unario=0;
  bool seguir=true;

  while (seguir){
    if (archivo->reachedEOF()){ // fin del archivo, devuelvo -1
      unario=-1;
      seguir=false;
    }
    else if (archivo->getBit()){ // leo un 1, devuelvo el unario
      seguir=false;
    }
    else { // leo un 0, incremento el unario
      unario++;
    }
  }

  return unario;
}

/*
// Crea el archivo "file_name" de tamano "bytes_size" bytes
// donde cada bit se elige siguiendo una distribucion Bernoulli~(prob_succ)
// con 0<prob_succ<1 y p(1)=prob_succ y p(0)=1-prob_succ
void crear_archivo_bernoulli(char* output_file_name, double prob_succ, int bytes_size){

  BitStreamWriter bitStreamWriter(output_file_name);

  int count_0s=0;
  int count_1s=0;
  int bits_size=8*bytes_size;

  srand(time(NULL)); // inicializa seed para rand()

  for(int i=0; i<bits_size; i++){
    // prob(value=1)=prob_succ, prob(value=0)=1-prob_succ
    int value=rand() <  prob_succ*((double)RAND_MAX + 1.0);

    if (value){
      bitStreamWriter.pushBit(1);
      count_1s++;
      //printf("1"); 
    }
    else {
      bitStreamWriter.pushBit(0);
      count_0s++;
      //printf("0");
    }
  }

  double porc_0s=((double)count_0s)/((double)bits_size);
  double porc_1s=((double)count_1s)/((double)bits_size);

  printf("0s=%d (%.2f) ---- 1s=%d (%.2f)\n\n",count_0s,porc_0s,count_1s,porc_1s);
}


// Lee el archivo "input_file_name" y cuenta ceros y unos
void leer_archivo_bernoulli(char* input_file_name){

  BitStreamReader bitStreamReader(input_file_name);

  int count_0s=0;
  int count_1s=0;

  while (!bitStreamReader.reachedEOF()){
    if (bitStreamReader.getBit()){
      count_1s++;
      printf("1");
    }
    else{
      count_0s++;
      printf("0");
    }
  }

  printf("\n0s=%d -- 1s=%d\n\n",count_0s,count_1s);
}


// Suma bit a bit dos archivos del mismo largo (0+0=0, 0+1=1+0=1, 1+1=1)
void sumar_dos_archivos(char* file1, char* file2, char* output_file_name){

  BitStreamReader bitStreamReader1(file1);
  BitStreamReader bitStreamReader2(file2);
  BitStreamWriter bitStreamWriter(output_file_name);

  while (!bitStreamReader1.reachedEOF()){
    if (bitStreamReader1.getBit()){
      if (bitStreamReader2.getBit()){
        bitStreamWriter.pushBit(1); // 1+1=1
      }
      else {
        bitStreamWriter.pushBit(1); // 0+1=1
      }
    }
    else {
      if (bitStreamReader2.getBit()){
        bitStreamWriter.pushBit(1); // 0+1=1
      }
      else {
        bitStreamWriter.pushBit(0); // 0+0=0
      }
    }
  }
}
*/
