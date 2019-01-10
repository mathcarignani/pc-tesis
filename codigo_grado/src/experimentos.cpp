#include "experimentos.h"
using namespace std;

// // ####################################################################################################### //
// // ################################# imprimir_rangos_golomb ############################################## //
// // ####################################################################################################### //

// calcula los primeros n rangos de golomb
void Experimentos::imprimir_rangos_golomb(int n){

  printf("     p      |   l  |   p_inf     |   p_sup     |  p_sup - p_inf    | esperanza_analitica | log_esperanza | l_aprox   |\n");
  printf("============+======+=============+=============+===================|=====================+===============+===========+\n");

  double p;
  int l;  
  double p_inf, p_sup;
  double diferencia;
  
  for (int i=1; i<=n; i++){

    p = pow(2,(double)-1/i); // p=2**(-1/cant). p in [ 0.5 , 0.7071067 , ... ]
    l=CodigoGolomb::calcular_l(p);
    CodigoGolomb::calcular_rango_p(l,p,p_inf,p_sup);
    diferencia=p_sup-p_inf;

    DistribucionGeo* distribucion_geo;
    distribucion_geo=new DistribucionGeo(p);
    double esperanza_analitica=distribucion_geo->esperanza_analitica();
    double log_esperanza_analitica=log(esperanza_analitica)/log(2);
    int l_aprox=(int) ceil(log_esperanza_analitica);

    Impresion::imprimir_double(p,7,1,11);

    printf("|");

    Impresion::imprimir_int(l,1,5);

    printf("|");

    Impresion::imprimir_double(p_inf,7,1,12);

    printf("|");

    Impresion::imprimir_double(p_sup,7,1,12);

    printf("|");

    Impresion::imprimir_double(diferencia,7,1,18);

    printf("|");

    Impresion::imprimir_double(esperanza_analitica,7,1,20);

    printf("|");

    Impresion::imprimir_double(log_esperanza_analitica,7,1,14);

    printf("|");

    Impresion::imprimir_int(l_aprox,1,10);

    printf("|");

    printf("\n");

  }
}


// // ####################################################################################################### //
// // ################################## comparar_codigos ################################################### //
// // ####################################################################################################### //

void imprimir_p(double delta_p, double p){
  if       (delta_p==0.01)    Impresion::imprimir_double(p,2,1,8);
  else if  (delta_p==0.001)   Impresion::imprimir_double(p,3,1,8);
  else if  (delta_p==0.0001)  Impresion::imprimir_double(p,4,1,8);
  else                        Impresion::imprimir_double(p,5,1,8);
}  

void Experimentos::actualizar_parametro_p(double & p, double & delta_p, int caso){

  // actualizo delta_p
  if ( (p>0.90 && p<=0.9997) && delta_p!=0.0001 ){
    delta_p=0.0001;
    if (caso==1){
      imprimir_columnas_codigo_huffman();  
    }
    else if (caso==2){
      imprimir_columnas_codigo_t();
    }
    else if (caso==3){
      imprimir_columnas_golomb_bn();
    }   
  }

  // actualizo p
  p+=delta_p;
}

void Experimentos::imprimir_columnas_codigo_golomb(){
  printf("=====================================+\n");
  printf("    p    | parametro l codigo golomb |\n");
  printf("=========+===========================+\n");
}

// "./app -experimento -golomb"
void Experimentos::golomb(){
  
  imprimir_columnas_codigo_golomb();

  // rango de p
  double p_inicial=0.5;
  double p_final=0.9999;
  double delta_p=0.001;

  int l; 
  double p=p_inicial;
  
  while (p<=p_final){

    l=CodigoGolomb::calcular_l(p);

    // IMPRIMO
    imprimir_p(delta_p,p);  printf("|");
    
    Impresion::imprimir_int(l,1,10);  printf("|");

    printf("\n");

    // actualizo p y el parametro delta_p
    actualizar_parametro_p(p,delta_p,4);
  }
}


void Experimentos::imprimir_columnas_codigo_huffman(){
  printf("=========================================================+=======================================+=========================\n");
  printf("         |                                               |              CODIGO HUFFMAN           |          tiempo         \n");
  printf("         |                                               |=======================================+=========================\n");
  printf("    p    | i_prima | lambda ||  entropia (E) | cant_simb |  largo md (E) | cant_simb | largo rel |  codigo    |   total    \n");
  printf("=========+=========+========++===============+===========+===============+===========+===========+============+============\n");
}

// "./app -experimento -huffman"
void Experimentos::huffman(){
  
  imprimir_columnas_codigo_huffman();

  // rango de p
  double p_inicial=0.5;
  double p_final=0.9997;
  double delta_p=0.001;
  
  // parametros distribucion binomial negativa
  DistribucionBN* distribucion_BN;
  double i_prima;
  int lambda;
  double entropia_practica;

  int cant_simbolos_tope=INT_MAX; // para que siempre me de error y obtener el maximo posible
  int cant_simbolos; // mayor cantidad posible de signos sin error de precision
  
  // parametros codigo huffman
  CodigoHuffman* codigo_huffman;
  int cant_simbolos_huffman; // cant_simbolos redondeado al multiplo de 10 menor mas cercano
  double largo_medio_huffman;
  double largo_relativo_huffman;

  // variables timer
  clock_t t_total,t_codigo;
  double tiempo_total,tiempo_codigo;

  double p=p_inicial;
  
  while (p<=p_final){

    // timer inicial
    t_total = clock();

    // creo una distribucion BN para el p actual
    distribucion_BN=new DistribucionBN(p);

    // calcula el i donde se anula la derivada de la funcion de probabilidad de la distribucion BN
    i_prima=distribucion_BN->calcular_i_prima();

    // calcula el minimo entero lambda>0 tal que P(0)>P(lambda), en el caso de la BN
    lambda=distribucion_BN->calcular_lambda(i_prima);

    // obtengo la entropia empirica lo mas aproximada posible (mayor cant_simbolos posible sin error de precision)
    cant_simbolos=cant_simbolos_tope;
    entropia_practica=distribucion_BN->calcular_entropia_practica(cant_simbolos);

    cant_simbolos_huffman=cant_simbolos-1;
    while ( cant_simbolos_huffman%10 != 0) cant_simbolos_huffman--;
    
    // CODIGO HUFFMAN
    t_codigo = clock();
    codigo_huffman=new CodigoHuffman(cant_simbolos_huffman,distribucion_BN,false,true);
    t_codigo = clock() - t_codigo;
    tiempo_codigo = ((double)t_codigo)/CLOCKS_PER_SEC; // in seconds

    largo_medio_huffman=codigo_huffman->largo_medio();
    largo_relativo_huffman=(largo_medio_huffman-entropia_practica)/entropia_practica;

    // timer final
    t_total = clock() - t_total;
    tiempo_total = ((double)t_total)/CLOCKS_PER_SEC; // in seconds

    // IMPRIMO
    imprimir_p(delta_p,p);  printf("|");

    Impresion::imprimir_double(i_prima,2,1,8);  printf("|");

    Impresion::imprimir_int(lambda,1,7);  printf("||");

    Impresion::imprimir_double(entropia_practica,10,1,14);  printf("|");

    Impresion::imprimir_int(cant_simbolos,1,10);  printf("|");

    Impresion::imprimir_double(largo_medio_huffman,10,1,14);  printf("|");

    Impresion::imprimir_int(cant_simbolos_huffman,1,10);  printf("|");

    Impresion::imprimir_double(largo_relativo_huffman,7,1,10);  printf("|");    

    Impresion::imprimir_double(tiempo_codigo,2,1,10); printf(" |");

    Impresion::imprimir_double(tiempo_total,2,1,11);

    printf("\n");

    // actualizo p y el parametro delta_p
    actualizar_parametro_p(p,delta_p,1);

  }
}

void Experimentos::imprimir_columnas_codigo_t(){
  printf("=========+================================+=========================\n");
  printf("         |           CODIGO T             |          tiempo         \n");
  printf("         +================================|=========================\n");
  printf("  p      |  alfa  | beta  |  largo md (A) |  codigo    |   total    \n");
  printf("=========+========+=======+===============+============+============\n");
}

// "./app -experimento -t"
void Experimentos::t(){
  
  imprimir_columnas_codigo_t();

  // rango de p
  double p_inicial=0.50;
  double p_final=0.9997;
  double delta_p=0.001;

  // parametros codigo T
  CodigoT* codigo_t;
  int alfa;
  int beta;
  double largo_medio_T;

  // variables timer
  clock_t t_total,t_codigo;
  double tiempo_total,tiempo_codigo;

  double p=p_inicial;
  
  while (p<=p_final){

    // timer inicial
    t_total = clock();

    // CODIGO T
    t_codigo = clock();
    codigo_t=new CodigoT(p,0,0); // paso alfa=0, beta=0 para que los calcule
    t_codigo = clock() - t_codigo;
    tiempo_codigo = ((double)t_codigo)/CLOCKS_PER_SEC; // in seconds

    alfa=codigo_t->get_alfa();
    beta=codigo_t->get_beta();
    largo_medio_T=codigo_t->largo_medio();

    // timer final
    t_total = clock() - t_total;
    tiempo_total = ((double)t_total)/CLOCKS_PER_SEC; // in seconds

    // IMPRIMO
    imprimir_p(delta_p,p);  printf("|");

    Impresion::imprimir_int(alfa,1,7);  printf("|");

    Impresion::imprimir_int(beta,1,6);  printf("|");

    Impresion::imprimir_double(largo_medio_T,10,1,14); printf("|");    

    Impresion::imprimir_double(tiempo_codigo,8,1,0);  printf(" |");

    Impresion::imprimir_double(tiempo_total,8,1,0); printf(" |");

    printf("\n");

    // actualizo p y el parametro delta_p
    actualizar_parametro_p(p,delta_p,2);
  }
}

void Experimentos::imprimir_columnas_golomb_bn(){
  printf("=========+===========================================+=========================+\n");
  printf("         |             CODIGO GOLOMB BN              |          tiempo         |\n");
  printf("         |===========================================|=========================+\n");
  printf("    p    |  esperanza    |     l     | largo md (A)  |  codigo    |   total    |\n");
  printf("=========+===============+===========+===============+============+============+\n");
}

// "./app -experimento -golomb_bn"
void Experimentos::golomb_bn(){
  
  imprimir_columnas_golomb_bn();

  // rango de p
  double p_inicial=0.5;
  double p_final=0.9997;
  double delta_p=0.001;

  // parametros codigo golomb mod
  CodigoGolombBN* codigo_golomb_bn;
  double esperanza;
  int l;
  double largo_medio_golomb_bn;

  // variables timer
  clock_t t_total,t_codigo;
  double tiempo_total,tiempo_codigo,tiempo_diez_ejecuciones;

  double p=p_inicial;
  
  while (p<=p_final){

    // timer inicial
    t_total = clock();

    // CODIGO T MOD
    // repito 10 veces y divido entre 10
    tiempo_diez_ejecuciones=0;
    for(int i=0; i<10; i++){
      t_codigo = clock();
      codigo_golomb_bn=new CodigoGolombBN(0,p);
      t_codigo = clock() - t_codigo;
      tiempo_diez_ejecuciones+=t_codigo;
    }
    tiempo_codigo = ((double)tiempo_diez_ejecuciones)/(10*CLOCKS_PER_SEC); // in seconds

    esperanza=codigo_golomb_bn->get_esperanza();
    l=codigo_golomb_bn->get_l();
    largo_medio_golomb_bn=codigo_golomb_bn->largo_medio();

    // timer final
    t_total = clock() - t_total;
    tiempo_total = ((double)t_total)/CLOCKS_PER_SEC; // in seconds

    // IMPRIMO
    imprimir_p(delta_p,p);  printf("|");
    
    Impresion::imprimir_double(esperanza,5,1,14); printf("|");

    Impresion::imprimir_int(l,1,10);  printf("|");

    Impresion::imprimir_double(largo_medio_golomb_bn,10,1,14);  printf("|");    

    Impresion::imprimir_double(tiempo_codigo,8,1,0);  printf(" |");

    Impresion::imprimir_double(tiempo_total,8,1,0); printf(" |");

    printf("\n");

    // actualizo p y el parametro delta_p
    actualizar_parametro_p(p,delta_p,3);
  }
}
