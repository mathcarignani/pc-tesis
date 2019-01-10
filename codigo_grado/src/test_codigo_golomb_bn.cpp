#include "test_codigo_golomb_bn.h"
using namespace std;

void TestCodigoGolombBN::test_largo_codigo_aux(int numero_test, double p){

  // creo el codigo golomb asociado al p dado
  CodigoGolombBN* codigo_golomb_bn;
  codigo_golomb_bn=new CodigoGolombBN(0,p);

  double largo_medio_analitico=codigo_golomb_bn->largo_medio();

  // creo una distribucion BN para el p actual
  DistribucionBN* distribucion_BN;
  distribucion_BN=new DistribucionBN(p);
  double largo_medio_empirico=TestAux::calcular_largo_medio_empirico(codigo_golomb_bn,distribucion_BN);

  bool exito;
  double dif=fabs(largo_medio_analitico-largo_medio_empirico);
  exito=(dif<0.0000000001);

  if (exito) {
    printf("[%d] exito - p=%.2f - largo_medio_analitico=%.6f, largo_medio_empirico=%.6f\n",numero_test,p,largo_medio_analitico,largo_medio_empirico);
  } 
  else   {
    printf("[%d] ERROR - p=%.2f - largo_medio_analitico=%.6f, largo_medio_empirico=%.6f\n",numero_test,p,largo_medio_analitico,largo_medio_empirico);
    exit(1);
  }     
}


void TestCodigoGolombBN::test_codigo_archivo_aux(int numero_test, double p, int cant_repeticiones){

  // creo el codigo golomb_bn asociado al p dado
  CodigoGolombBN* codigo_golomb_bn;
  codigo_golomb_bn=new CodigoGolombBN(0,p);

  // se generan enteros equiprobables en el rango [0,2*l-1]
  // para probar los dos metodos de codificacion, es decir para i<l y para i>l
  int maximo=2*codigo_golomb_bn->get_l()-1;
  if (maximo<50){
    maximo=50; // para evitar rangos demasiado chicos donde siempre se generan los mismos simbolos
  }

  vector <int> vector_chequeo(cant_repeticiones,0); // vector utilizado para chequear

  // codifico archivo
  TestAux::crear_archivo_codificado(codigo_golomb_bn,vector_chequeo,maximo,cant_repeticiones);

  // decodifico archivo
  bool exito=false;
  exito=TestAux::decodificar_archivo(codigo_golomb_bn,vector_chequeo,cant_repeticiones);

  // si son iguales los archivos la codificacion y decodificacion fue correcta
  if (exito) {
    printf("[%d] exito - p=%.2f, l=%d, maximo=%d\n",numero_test,p,codigo_golomb_bn->get_l(),maximo);
  } 
  else {
    printf("[%d] ERROR - p=%.2f, l=%d, maximo=%d\n",numero_test,p,codigo_golomb_bn->get_l(),maximo);
    exit(1);
  }       

}

// ####################################################################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

// testea que el largo de codigo calculado analiticamente
// es igual al largo de codigo empirico para una cantidad grande de simbolos
void TestCodigoGolombBN::test_largo_codigo(){

  // testeo para cada uno de estos valores de p
  double ps[11]={0.10,0.50,0.60,0.70,0.80,0.85,0.90,0.95,0.96,0.97,0.98};

  for(int i=0; i<11; i++){
    test_largo_codigo_aux(i+1,ps[i]);
  }

}

void TestCodigoGolombBN::test_esperanza(){
  double p_inicial=0.60;
  double p_final=0.99;
  double delta_p=0.01;

  double esperanza_teorica;
  double esperanza_practica;

  int param_practica=100;
  int param_practica_anterior;
  int param_maximo=1000000;
  int lambda;
  double dif;

  bool seguir;
  bool falla;
  bool exito;

  double p;
  for (p=p_inicial; p<=p_final; p+=delta_p){

    // creo el codigo golomb asociado al p dado
    CodigoGolombBN* codigo_golomb_bn;
    codigo_golomb_bn=new CodigoGolombBN(0,p);

    // calculo la esperanza teorica
    esperanza_teorica=codigo_golomb_bn->get_esperanza();

    // calculo la esperanza practica en el intervalo [0,param_practica]
    lambda=codigo_golomb_bn->get_lambda();
    esperanza_practica=codigo_golomb_bn->calcular_esperanza_practica(0,lambda-1);
    param_practica = lambda-1;
    //printf("esperanza en [0,%d] = %.5f\n",lambda-1,esperanza_practica);
    dif=1;
    falla=false;
    exito=false;

    while (( seguir =  !( falla || exito ) )){
      param_practica_anterior=param_practica;
      param_practica*=10;

      if (param_practica>=param_maximo){
        falla=true;
      }
      else {
        // calculo la esperanza practica en el intervalo [param_practica_anterior+1,param_practica]
        esperanza_practica+=codigo_golomb_bn->calcular_esperanza_practica(param_practica_anterior+1,
                                                                          param_practica);
        //printf("esperanza en [%d,%d] = %.5f\n",param_practica_anterior+1,param_practica,esperanza_practica);
        
        dif=fabs(esperanza_teorica-esperanza_practica);
        exito=(dif<0.000001);
      }
    }

    if (falla){
      printf("ERROR test_esperanza >> ");
      printf("p=%.2f => esperanza_teorica = %.5f, esperanza_practica = %.5f\n",p,esperanza_teorica,esperanza_practica);
      exit(1);
    }
    else {
      printf("exito - p=%.2f => esperanza_teorica = %.5f, esperanza_practica = %.5f\n",p,esperanza_teorica,esperanza_practica);
    }
  }

  if (!falla && exito) {
    printf("EXITO test_esperanza para p in [%.2f,%.2f]\n",p_inicial,p_final);
  }

}


// chequea que el vector vector_perm se cree de forma correcta:
// [1] el simbolo con menor probabilidad tiene indice 0
// [2] P(lambda)<=P(0)
// [3] P(lambda-1)>P(0) cuando lambda>1
void TestCodigoGolombBN::test_vector_perm(){
  double p_inicial=0.5;
  double p_final=0.999;
  double delta_p=0.001;
  
  double i_prima;
  int lambda;
  bool exito1;
  bool exito11;
  bool exito2;
  bool exito3;
  bool error;
  double p;

  for (p=p_inicial; p<=p_final; p+=delta_p){
    
    // creo una distribucion BN
    DistribucionBN* distribucion_bn=new DistribucionBN(p);

    // a partir de la distribucion obtengo el vector lambda
    vector <unsigned int> vector_perm;
    vector <unsigned int> vector_perm_inverso;
    vector_perm=distribucion_bn->calcular_vector_perm(i_prima,lambda);
    vector_perm_inverso=distribucion_bn->calcular_vector_perm_inverso(vector_perm,lambda);
    //for (int i=0; i<lambda; i++){
    //  printf("lambda[%d] = %d\n",i,(int)vector_perm[i]);
    //}

    exito1=((int)vector_perm[0]==(lambda-1));
    exito11=((int)vector_perm_inverso[lambda-1]==0);
    exito2=(lambda==1)||(distribucion_bn->prob(lambda)<distribucion_bn->prob(0));
    exito3=(lambda==1)||(distribucion_bn->prob(lambda-1)>distribucion_bn->prob(0));

    error=(! (exito1 && exito11 && exito2 && exito3) );

    // chequeo si hubo error
    if ( error ) break;
    //printf("1");
  }

  if (error) {
    printf("ERROR test_vector_perm >> p=%.4f",p);
    exit(1);
  } 
  else   {
    printf("EXITO test_vector_perm.\n");
  }     
}

// testea que funcionan correctamente la codificacion y decodificacion
void TestCodigoGolombBN::test_codigo_archivo(){

  // testeo que el codigo codifica y decodifica de forma correcta para
  // cada uno de estos valores de p
  double ps[11]={0.10,0.50,0.60,0.70,0.80,0.85,0.90,0.95,0.96,0.97,0.98};

  int cant_repeticiones=100; // la cantidad de simbolos que codifico y decodifico

  for(int i=0; i<11; i++){
    test_codigo_archivo_aux(i+1,ps[i],cant_repeticiones);
  }
}
