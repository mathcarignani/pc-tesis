#include "test_codigo_golomb.h"
using namespace std;

// ####################################################################################################### //
// ################## auxiliares de TestCodigoGolomb::test_codigo() ###################################### //
// ####################################################################################################### //

bool TestCodigoGolomb::comparar_codigos(vector <PalabraDeCodigo*> codigo_golomb_1,
                                        CodigoGolomb* codigo_golomb_2,
                                        int cant_simbolos){
  int unario;
  bool antes;
  PalabraDeCodigo* palabra1;
  PalabraDeCodigo* palabra2_aux;
  PalabraDeCodigo* palabra2;

  bool seguir=true;
  int i=0;

  while (seguir && i<cant_simbolos){

    palabra1=codigo_golomb_1[i];

    // palabra es NULL si el parametro l es 1
    palabra2_aux=codigo_golomb_2->codificar_simbolo(i,unario,antes);
    palabra2=PalabraDeCodigo::concatenar_unario(palabra2_aux,unario,antes);

    //printf("palabra1=");palabra1->imprimir_palabra();printf(" - ");
    //printf("palabra2=");palabra2->imprimir_palabra();printf("\n");

    seguir=palabra1->comparar_palabras(palabra2);

    i++;
  }

  return seguir;
}

void TestCodigoGolomb::test_golomb(int enteros[], int largos[], int l,
                                   int cant_simbolos, int numero_test){

  vector <PalabraDeCodigo*> codigo_golomb_1=TestAux::crear_codigo(enteros,largos,cant_simbolos);

  CodigoGolomb* codigo_golomb_2=new CodigoGolomb(l,-1,false,-1);

  //codigo_golomb_2->mostrar_codigo();

  bool iguales;
  iguales=comparar_codigos(codigo_golomb_1,codigo_golomb_2,cant_simbolos);

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

void TestCodigoGolomb::test_largo_codigo_aux(int numero_test, double p){

  // creo el codigo golomb asociado al p dado
  CodigoGolomb* codigo_golomb;
  codigo_golomb=new CodigoGolomb(0,p,false,-1);

  double largo_medio_analitico=codigo_golomb->largo_medio();

  // creo una distribucion Geo para el p actual
  DistribucionGeo* distribucion_geo;
  distribucion_geo=new DistribucionGeo(p);
  double largo_medio_empirico=TestAux::calcular_largo_medio_empirico(codigo_golomb,distribucion_geo);

  bool exito;
  double dif=fabs(largo_medio_analitico-largo_medio_empirico);
  exito=(dif<0.0000000001);

  //printf("largo_medio_analitico=%.6f, largo_medio_empirico=%.6f\n",largo_medio_analitico,largo_medio_empirico);
  
  if (exito) {
    printf("[%d] exito - p=%.2f\n",numero_test, p);
  } 
  else {
    printf("[%d] ERROR - p=%.2f\n",numero_test, p);
    exit(1);
  }       
  
}

void TestCodigoGolomb::test_codigo_archivo_aux(int numero_test, int l, int cant_repeticiones){

  // creo el codigo golomb con parametro l
  CodigoGolomb* codigo_golomb;
  codigo_golomb=new CodigoGolomb(l,-1,false,-1);

  // se generan enteros equiprobables en el rango [0,2*l-1]
  // para probar los dos metodos de codificacion, es decir para i<l y para i>l
  int maximo=2*codigo_golomb->get_l()-1;
  if (maximo<50){
    maximo=50; // para evitar rangos demasiado chicos donde siempre se generan los mismos simbolos
  }

  vector <int> vector_chequeo(cant_repeticiones,0); // vector utilizado para chequear

  // codifico archivo
  TestAux::crear_archivo_codificado(codigo_golomb,vector_chequeo,maximo,cant_repeticiones);

  // decodifico archivo
  bool exito=false;
  exito=TestAux::decodificar_archivo(codigo_golomb,vector_chequeo,cant_repeticiones);

  // si son iguales los archivos la codificacion y decodificacion fue correcta
  if (exito)  {
    printf("[%d] exito - l=%d, maximo=%d\n",numero_test,codigo_golomb->get_l(),maximo);
  }
  else   {
    printf("[%d] ERROR - l=%d, maximo=%d\n",numero_test,codigo_golomb->get_l(),maximo);
    exit(1);
  }     
}

// ####################################################################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

// testea que funcionan correctamente la codificacion y decodificacion
void TestCodigoGolomb::test_codigo(){

/*************************************
  TEST 1: l=1 (ejemplo Golomb 1966)

    x  |  c(x)
  ----------------------
    0  |  1
    1  |  01
    2  |  001 
    3  |  0001
    4  |  00001
    5  |  000001
    6  |  0000001
    7  |  00000001
    8  |  000000001
    9  |  0000000001
    10 |  00000000001
**************************************/
  int l=1;
  int cant_simbolos=11;
  int enteros[11]={1,1,1,1,1,1,1,1,1,1 ,1};
  int  largos[11]={1,2,3,4,5,6,7,8,9,10,11};
  test_golomb(enteros,largos,l,cant_simbolos,1);

/*************************************
  TEST 2: l=2 (ejemplo Golomb 1966)

    x  |  c(x)
  ----------------------
    0  |  10
    1  |  11
    2  |  010 
    3  |  011
    4  |  0010
    5  |  0011
    6  |  00010
    7  |  00011
    8  |  000010
    9  |  000011
    10 |  0000010
**************************************/
  int l_2=2;
  int cant_simbolos_2=11;
  int enteros_2[11]={2,3,2,3,2,3,2,3,2,3,2};
  int  largos_2[11]={2,2,3,3,4,4,5,5,6,6,7}; // series de 2 largos iguales
  test_golomb(enteros_2,largos_2,l_2,cant_simbolos_2,2);  

/*************************************
  TEST 3: l=3 (ejemplo Golomb 1966)

    x  |  c(x)
  ----------------------
    0  |  10
    1  |  110
    2  |  111 
    3  |  010
    4  |  0110
    5  |  0111
    6  |  0010
    7  |  00110
    8  |  00111
    9  |  00010
    10 |  000110
**************************************/
  int l_3=3;
  int cant_simbolos_3=11;
  int enteros_3[11]={2,6,7,2,6,7,2,6,7,2,6};
  int  largos_3[11]={2,
                     3,3,3, // series de 3 largos iguales
                     4,4,4,
                     5,5,5,
                     6};
  test_golomb(enteros_3,largos_3,l_3,cant_simbolos_3,3);    

/*************************************
  TEST 4: l=4 (ejemplo Golomb 1966)

    x  |  c(x)
  ----------------------
    0  |  100
    1  |  101
    2  |  110
    3  |  111
    4  |  0100
    5  |  0101
    6  |  0110
    7  |  0111
    8  |  00100
    9  |  00101
    10 |  00110
**************************************/
  int l_4=4;
  int cant_simbolos_4=11;
  int enteros_4[11]={4,5,6,7,4,5,6,7,4,5,6};
  int  largos_4[11]={3,3,3,3, // series de 4 largos iguales
                     4,4,4,4,
                     5,5,5};
  test_golomb(enteros_4,largos_4,l_4,cant_simbolos_4,4);  

/*************************************
  TEST 5: l=14 (ejemplo Golomb 1966)

    x  |  c(x)
  ----------------------
    0  |  1000
    1  |  1001
    2  |  10100
    3  |  10101
    4  |  10110
    5  |  10111
    6  |  11000
    7  |  11001
    8  |  11010
    9  |  11011
    10 |  11100
    11 |  11101
    12 |  11110
    13 |  11111
    14 |  01000
    15 |  01001
    16 |  010100
    17 |  010101
    18 |  010110
    19 |  010111
    20 |  011000
    21 |  011001
    22 |  011010
    23 |  011011
    24 |  011100
    25 |  011101
    26 |  011110
    27 |  011111
    28 |  001000
    29 |  001001
    30 |  0010100
    31 |  0010101
    32 |  0010110
    33 |  0010111
    34 |  0011000
    35 |  0011001
    36 |  0011010
    37 |  0011011
    38 |  0011100
    39 |  0011101
    40 |  0011110
    41 |  0011111
    42 |  0001000
    43 |  0001001
    44 |  00010100
    45 |  00010101
    46 |  00010110
    47 |  00010111        
**************************************/
  int l_5=14;
  int cant_simbolos_5=48;
  int enteros_5[48]={8,9,20,21,22,23,24,25,26,27,28,29,30,31,
                     8,9,20,21,22,23,24,25,26,27,28,29,30,31,
                     8,9,20,21,22,23,24,25,26,27,28,29,30,31,
                     8,9,20,21,22,23};
  int  largos_5[48]={4,4,
                     5,5,5,5,5,5,5,5,5,5,5,5,5,5, // series de 14 largos iguales
                     6,6,6,6,6,6,6,6,6,6,6,6,6,6,
                     7,7,7,7,7,7,7,7,7,7,7,7,7,7,
                     8,8,8,8};
  test_golomb(enteros_5,largos_5,l_5,cant_simbolos_5,5);

/*************************************
  TEST 6: l=16 (ejemplo Golomb 1966)

    x  |  c(x)
  ----------------------
    0  |  10000
    1  |  10001
    2  |  10010
    3  |  10011
    4  |  10100
    5  |  10101
    6  |  10110
    7  |  10111
    8  |  11000
    9  |  11001
    10 |  11010
    11 |  11011
    12 |  11100
    13 |  11101
    14 |  11110
    15 |  11111
    16 |  010000
    17 |  010001
    18 |  010010
    19 |  010011
    20 |  010100
    21 |  010101
    22 |  010110
    23 |  010111
    24 |  011000
    25 |  011001
    26 |  011010
    27 |  011011
    28 |  011100
    29 |  011101
    30 |  011110
    31 |  011111
    32 |  0010000
    33 |  0010001
    34 |  0010010
    35 |  0010011
    36 |  0010100
    37 |  0010101
    38 |  0010110
    39 |  0010111
    40 |  0011000
    41 |  0011001
    42 |  0011010
    43 |  0011011
    44 |  0011100
    45 |  0011101
    46 |  0011110
    47 |  0011111        
**************************************/
  int l_6=16;
  int cant_simbolos_6=48;
  int enteros_6[48]={16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
                     16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
                     16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31};
  int  largos_6[48]={5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5, // series de 16 largos iguales
                     6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
                     7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7};
  test_golomb(enteros_6,largos_6,l_6,cant_simbolos_6,6);    
}

// testea que el largo de codigo calculado analiticamente
// es igual al largo de codigo empirico para una cantidad grande de simbolos
void TestCodigoGolomb::test_largo_codigo(){

  // testeo para cada uno de estos valores de p
  double ps[11]={0.10,0.50,0.60,0.70,0.80,0.85,0.90,0.95,0.96,0.97,0.98};

  for(int i=0; i<11; i++){
    test_largo_codigo_aux(i+1,ps[i]);
  }

}

// testea que funcionan correctamente la codificacion y decodificacion
void TestCodigoGolomb::test_codigo_archivo(){

  // testeo que el codigo codifica y decodifica de forma correcta para
  // cada uno de estos valores de l
  double ps[11]={1,2,3,5,8,10,15,20,25,30,50};

  int cant_repeticiones=100; // la cantidad de simbolos que codifico y decodifico

  for(int i=0; i<11; i++){
    test_codigo_archivo_aux(i+1,ps[i],cant_repeticiones);
  }
}
