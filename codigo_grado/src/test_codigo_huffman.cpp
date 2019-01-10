#include "test_codigo_huffman.h"
using namespace std;

// ####################################################################################################### //
// ########################################### auxiliares ################################################ //
// ####################################################################################################### //
  
vector <double> TestCodigoHuffman::crear_probabilidades(double probs[], int cant_simbolos){
  vector <double> probabilidades;

  for (int i=0; i<cant_simbolos; i++){
    probabilidades.push_back(probs[i]);
  }
  return probabilidades;
}

bool TestCodigoHuffman::comparar_codigos(vector <PalabraDeCodigo*> codigo_huffman_1,
                                         CodigoHuffman* codigo_huffman_2){
  PalabraDeCodigo* palabra1;
  PalabraDeCodigo* palabra2;

  bool seguir=true;
  int i=0;
  int cant_simbolos=codigo_huffman_2->get_cantidad_simbolos();

  while (seguir && i<cant_simbolos) {
    palabra1=codigo_huffman_1[i];
    
    int dummy1; bool dummy2;
    palabra2=codigo_huffman_2->codificar_simbolo(i,dummy1,dummy2);

    //printf("palabra1=");palabra1->imprimir_palabra();printf(" - ");
    //printf("palabra2=");palabra2->imprimir_palabra();printf("\n");

    seguir=palabra1->comparar_palabras(palabra2);
    
    i++;
  }
  return seguir;
}

void TestCodigoHuffman::test_huffman(int enteros[], int largos[], double probs[],
                                     int cant_simbolos, int numero_test){
  
  vector <PalabraDeCodigo*> codigo_huffman_1=TestAux::crear_codigo(enteros,largos,cant_simbolos);
    
  vector <double> probabilidades=crear_probabilidades(probs,cant_simbolos);
  
  CodigoHuffman* codigo_huffman_2;
  codigo_huffman_2=new CodigoHuffman(cant_simbolos,probabilidades,false,false);
  
  //codigo_huffman_2->mostrar_codigo();

  bool iguales;
  iguales=comparar_codigos(codigo_huffman_1,codigo_huffman_2);

  if (iguales){
    printf("[%d] exito\n",numero_test);
  }
  else {
    printf("[%d] ERROR\n",numero_test);
    exit(1);
  }         
}

// ####################################################################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

void TestCodigoHuffman::test(){
  
/*************************************
  TEST 1: ejemplo 5.6.1 del Cover

    x  |  p(x)  |  c(x)
  -----------------------
    0  |  0.25  |  00
    1  |  0.25  |  10
    2  |  0.20  |  01
    3  |  0.15  |  110
    4  |  0.15  |  111
**************************************/   
  int cant_simbolos=5;  
  int enteros[5]={0,2,1,6,7};
  int  largos[5]={2,2,2,3,3};
  double probs[5]={0.25,0.25,0.20,0.15,0.15};
  test_huffman(enteros,largos,probs,cant_simbolos,1);

/*************************************
  TEST 2: ejercicio 5.2 del Cover

    x  |  p(x)  |  c(x)
  -----------------------
    0  |  0.49  |  0
    1  |  0.26  |  10
    2  |  0.12  |  110
    3  |  0.04  |  11100
    4  |  0.04  |  11101
    5  |  0.03  |  11110
    6  |  0.02  |  11111      
**************************************/    
  int cant_simbolos_2=7;  
  int enteros_2[7]={0,2,6,28,29,30,31};
  int  largos_2[7]={1,2,3,5, 5, 5, 5};
  double probs_2[7]={0.49,0.26,0.12,0.04,0.04,0.03,0.02};
  test_huffman(enteros_2,largos_2,probs_2,cant_simbolos_2,2);

/*************************************
  TEST 3: ejercicio 5.5(a) del Cover

    x  |  p(x)  |  c(x)
  -----------------------
    0  |  1/3   |  00
    1  |  1/5   |  10
    2  |  1/5   |  11
    3  |  2/15  |  010
    4  |  2/15  |  011    
**************************************/    
  int cant_simbolos_3=5;  
  int enteros_3[5]={0,2,3,2,3};
  int  largos_3[5]={2,2,2,3,3};
  double probs_3[5]={(double)1/3,(double)1/5,(double)1/5,(double)2/15,(double)2/15};
  test_huffman(enteros_3,largos_3,probs_3,cant_simbolos_3,3);  

/*************************************
  TEST 4: ejercicio 5.5(b) del Cover

    x  |  p(x) |  c(x)
  -----------------------
    0  |  1/5  |  000
    1  |  1/5  |  001
    2  |  1/5  |  10
    3  |  1/5  |  11
    4  |  1/5  |  01   
**************************************/    
  int cant_simbolos_4=5;  
  int enteros_4[5]={0,1,2,3,1};
  int  largos_4[5]={3,3,2,2,2};
  double probs_4[5]={(double)1/5,(double)1/5,(double)1/5,(double)1/5,(double)1/5};
  test_huffman(enteros_4,largos_4,probs_4,cant_simbolos_4,4);    

/*************************************
  TEST 5: ejercicio 5.32 del Cover

    x  |  p(x) |  c(x)
  -----------------------
    0  |  8/23 |  00
    1  |  6/23 |  01
    2  |  4/23 |  10
    3  |  2/23 |  1100
    4  |  2/23 |  111
    5  |  1/23 |  1101
**************************************/    
  int cant_simbolos_5=6;  
  int enteros_5[6]={0,1,2,12,7,13};
  int  largos_5[6]={2,2,2,4, 3, 4};
  double probs_5[6]={(double)8/23,(double)6/23,(double)4/23,(double)2/23,(double)2/23,(double)1/23};
  test_huffman(enteros_5,largos_5,probs_5,cant_simbolos_5,5);  

/*************************************
  TEST 6: Ejercicio 1 Practico 2 CDP

    x  |  p(x) |  c(x)
  -----------------------
    0  |  0.30 |  00
    1  |  0.20 |  10
    2  |  0.15 |  010
    3  |  0.15 |  011
    4  |  0.10 |  110
    5  |  0.10 |  111
**************************************/    
  int cant_simbolos_6=6;  
  int enteros_6[6]={0,2,2,3,6,7};
  int  largos_6[6]={2,2,3,3,3,3};
  double probs_6[6]={0.30,0.20,0.15,0.15,0.10,0.10};
  test_huffman(enteros_6,largos_6,probs_6,cant_simbolos_6,6);    

/*************************************
  TEST 7: Ejercicio 1 Practico 2 CDP

    x  |  p(x) |  c(x)
  -----------------------
    0  |  0.30 |  00
    1  |  0.25 |  10
    2  |  0.15 |  010
    3  |  0.10 |  110
    4  |  0.10 |  111
    5  |  0.05 |  0110
    6  |  0.05 |  0111    
**************************************/    
  int cant_simbolos_7=7;  
  int enteros_7[7]={0,2,2,6,7,6,7};
  int  largos_7[7]={2,2,3,3,3,4,4};
  double probs_7[7]={0.30,0.25,0.15,0.10,0.10,0.05,0.05};
  test_huffman(enteros_7,largos_7,probs_7,cant_simbolos_7,7);    


/*************************************
  TEST 8: Ejercicio 4 Practico 2 CDP

    x  |  p(x) |  c(x)
  -----------------------
    0  |  1/3  |  00
    1  |  1/3  |  01
    2  |  1/4  |  10
    3  |  1/12 |  11      
**************************************/    
  int cant_simbolos_8=4;  
  int enteros_8[4]={0,1,2,3};
  int  largos_8[4]={2,2,2,2};
  double probs_8[4]={(double)1/3,(double)1/3,(double)1/4,(double)1/12};
  test_huffman(enteros_8,largos_8,probs_8,cant_simbolos_8,8);            
  
}
