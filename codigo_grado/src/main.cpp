#include <cstring>
#include <iostream>
#include <stdlib.h>

#include "experimentos.h"
#include "procedimientos.h"
#include "test.h"
using namespace std;

// int comando
#define mostrar 1
#define imprimir 2
#define experimento 3
#define test 4

// int codigo
#define codigo_golomb 1
#define codigo_golomb_bn 2
#define codigo_huffman 3
#define codigo_t 4

bool esY(char* entrada){
  return (strcmp(entrada,"Y") == 0);
}

bool esBN(char* entrada){
  return (strcmp(entrada,"BN") == 0);
}

int leer_comando(char* entrada){
  int comando=0;
  if      (strcmp(entrada,"-mostrar") == 0) comando=mostrar;
  else if (strcmp(entrada,"-imprimir") == 0) comando=imprimir;
  else if (strcmp(entrada,"-experimento") == 0) comando=experimento;
  else if (strcmp(entrada,"-test") == 0) comando=test;
  return comando;
}

int leer_codigo(char* entrada){
  int codigo=0;
  if      (strcmp(entrada,"-golomb") == 0) codigo=codigo_golomb;
  else if (strcmp(entrada,"-golomb_bn") == 0) codigo=codigo_golomb_bn;
  else if (strcmp(entrada,"-huffman") == 0) codigo=codigo_huffman;
  else if (strcmp(entrada,"-t") == 0) codigo=codigo_t;
  return codigo;
}

void imprimir_comando(int comando, int codigo){
  if (comando==mostrar)          printf("-mostrar");
  else if (comando==imprimir)    printf("-imprimir");
  else if (comando==experimento) printf("-experimento");
  else if (comando==test)        printf("-test");

  if (codigo==codigo_golomb)          printf(" -golomb");
  else if (codigo==codigo_golomb_bn)  printf(" -golomb_bn");
  else if (codigo==codigo_huffman)    printf(" -huffman");
  else if (codigo==codigo_t)          printf(" -t");
}

int main(int argc, char *argv[]){
  
  // imprimo entrada al main
  for(int i=0; i<argc; i++){
    cout << argv[i] << " ";
  }
  cout << endl << endl;

  int no_leidos=argc-1; // resto la cadena "./app"
  int j=1; // indice de la proxima entrada que se va a leer

  if (no_leidos==0){
    printf("ERROR: Se debe especificar un comando.\n;");
    return -1;
  }
  
  // leo el comando
  int comando=leer_comando(argv[j++]);
  no_leidos--;

  if (comando==0){
    printf("ERROR: Comando invalido.\n");
    return -1;
  }

  if (no_leidos==0){

    if (comando==test){
      Test::todos_los_tests(); // "./app -test"
      return 0;
    }
    else {
      printf("ERROR: Faltan parametros para ejecutar el comando ");
      imprimir_comando(comando,0);
      printf(".\n");
      return -1;
    }

  }

  if (comando==experimento){

    char* experim=argv[j++];

    // "./app -experimento -huffman"
    if (strcmp(experim,"-huffman") == 0){
      Experimentos::huffman();
      return 0;
    } 
    // "./app -experimento -t"
    else if (strcmp(experim,"-t") == 0){
      Experimentos::t();
      return 0;
    } 
    // "./app -experimento -golomb_bn"
    else if (strcmp(experim,"-golomb_bn") == 0){
      Experimentos::golomb_bn();
      return 0;
    }  
    // "./app -experimento -golomb"
    else if (strcmp(experim,"-golomb") == 0){
      Experimentos::golomb();
      return 0;
    }        
    // "./app -experimento -rangos 10"
    else if (strcmp(experim,"-rangos") == 0){
      int n=atoi(argv[j++]);
      Experimentos::imprimir_rangos_golomb(n);
      return 0;
    } 
  }

  // defino los 5 parametros del comando -imprimir
  int cant_simbolos;
  bool BN;
  double p;
  bool imprimir_probs;
  bool imprimir_perfil;

  if (comando==imprimir) {

    if (no_leidos<5){
      printf("ERROR: Faltan parametros para ejecutar el comando ");
      imprimir_comando(comando,0);
      printf(".\n");
      return -1;
    }
    
    // leo los 5 parametros del comando -imprimir
    cant_simbolos=atoi(argv[j++]);
    BN=esBN(argv[j++]);
    p=atof(argv[j++]);
    imprimir_probs=esY(argv[j++]);
    imprimir_perfil=esY(argv[j++]);

    no_leidos-=5;
  }

  if ( comando==mostrar || comando==imprimir || comando==test ){

    if (no_leidos==0){
      printf("ERROR: Faltan parametros para ejecutar el comando ");
      imprimir_comando(comando,0);
      printf(".\n");
      return -1;
    }

    // leo el codigo
    int codigo=leer_codigo(argv[j++]);
    no_leidos--;

    if (codigo==0){
      printf("ERROR: Codigo invalido.\n");
      return -1;
    }

    if (comando==test){

      if (codigo==codigo_golomb)          Test::test_codigo_golomb();  // "./app -test -golomb"
      else if (codigo==codigo_golomb_bn)  Test::test_codigo_golomb_bn();  // "./app -test -golomb_bn"
      else if (codigo==codigo_huffman)    Test::test_codigo_huffman(); // "./app -test -huffman"
      else if (codigo==codigo_t)          Test::test_codigo_t();   // "./app -test -T"
      return 0;
    }

    if (no_leidos==0){
      printf("ERROR: Faltan parametros para ejecutar el comando ");
      imprimir_comando(comando,codigo);
      printf(".\n");
      return -1;
    }

    if (comando==experimento){
      return 0;
    }

    // if (comando==mostrar || comando==imprimir)

    if (codigo==codigo_golomb) {        

      int l=atoi(argv[j++]);
      // solo leo la p si l==0
      double p_=(l==0) ? atof(argv[j++]) : -1;

      if (comando==mostrar){
        /*  EJEMPLOS:
          ./app -mostrar -golomb 10
          ./app -mostrar -golomb 0 0.9
        */
        Procedimientos::mostrar_codigo_golomb(l,p_);
      }
      else if (comando==imprimir){
        /*  EJEMPLOS:
          ./app -imprimir 100 BN 0.9 Y Y -golomb 10
          ./app -imprimir 100 Geo 0.9 N Y -golomb 0 0.9
        */
        Procedimientos::imprimir_codigo_golomb(l,p_,
                                               cant_simbolos,BN,p,
                                               imprimir_probs,imprimir_perfil);
      }
    }
    else if (codigo==codigo_golomb_bn){

      if (no_leidos<2){
        printf("ERROR: Faltan parametros para ejecutar el comando ");
        imprimir_comando(comando,codigo);
        printf(".\n");
        return -1;
      }

      int l=atoi(argv[j++]);
      double p_=atof(argv[j++]);

      if (comando==mostrar){
        /*  EJEMPLOS:
          ./app -mostrar -golomb_bn 10 0.9
          ./app -mostrar -golomb_bn 1 0.9
        */
        Procedimientos::mostrar_codigo_golomb_bn(l,p_);
      }
      else if (comando==imprimir){
        /*  EJEMPLOS:
          ./app -imprimir 100 BN 0.9 Y Y -golomb_bn 10
          ./app -imprimir 100 Geo 0.9 N Y -golomb_bn 0 0.9
        */
        Procedimientos::imprimir_codigo_golomb_bn(l,p_,
                                                   cant_simbolos,BN,p,
                                                   imprimir_probs,imprimir_perfil);
      }
    }
    else if (codigo==codigo_huffman){

      if (no_leidos<3){
        printf("ERROR: Faltan parametros para ejecutar el comando ");
        imprimir_comando(comando,codigo);
        printf(".\n");
        return -1;
      }

      bool BN_=esBN(argv[j++]); 
      double p_=atof(argv[j++]);
      int cant_simbolos_=atoi(argv[j++]);      

      if (comando==mostrar){
        /*  EJEMPLOS:
          ./app -mostrar -huffman BN 0.9 100
          ./app -mostrar -huffman Geo 0.95 50
        */
        Procedimientos::mostrar_codigo_huffman(BN_,p_,cant_simbolos_);  
      }
      else if (comando==imprimir){
        /*  EJEMPLOS:
          ./app -imprimir 100 BN 0.9 Y Y -huffman BN 0.9 100
          ./app -imprimir 100 Geo 0.9 N Y -huffman Geo 0.95 50
        */
        Procedimientos::imprimir_codigo_huffman(BN_,p_,cant_simbolos_,
                                                cant_simbolos,BN,p,
                                                imprimir_probs,imprimir_perfil);
      }
    }
    else if (codigo==codigo_t){

      double p_=atof(argv[j++]);
      no_leidos--;

      int alfa, beta;
      if (no_leidos==0){
        alfa=0; beta=0;
      }
      else {
        alfa=atoi(argv[j++]);
        beta=atoi(argv[j++]);
      }

      if (comando==mostrar){
        /*  EJEMPLOS:
          ./app -mostrar -t 0.9
          ./app -mostrar -t 0.9 10 5
        */
        Procedimientos::mostrar_codigo_t(p_,alfa,beta);
      }
      else if (comando==imprimir){
        /*  EJEMPLOS:
          ./app -imprimir 100 BN 0.9 Y Y -t 0.9
          ./app -imprimir 100 Geo 0.9 N Y -t 0.9 10 5
        */
        Procedimientos::imprimir_codigo_t(p_,alfa,beta,
                                              cant_simbolos,BN,p,
                                              imprimir_probs,imprimir_perfil);
      }
    }
    return 0;
  }
}

