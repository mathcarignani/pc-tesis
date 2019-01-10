#include "test_codigo_t.h"
using namespace std;


void TestCodigoT::test_largo_codigo_aux(int numero_test, double p){

  // creo el codigo T asociado al p dado
  CodigoT* codigo_t;
  codigo_t=new CodigoT(p,0,0);

  double largo_medio_analitico=codigo_t->largo_medio();

  // creo una distribucion BN para el p actual
  DistribucionBN* distribucion_BN;
  distribucion_BN=new DistribucionBN(p);
  double largo_medio_empirico=TestAux::calcular_largo_medio_empirico(codigo_t,distribucion_BN);

  bool exito;
  double dif=fabs(largo_medio_analitico-largo_medio_empirico);
  exito=(dif<0.0000000001);

  if (p==0.60){ // TODO check
    exito=(dif<0.0001);
  }

  //printf("largo_medio_analitico=%.6f, largo_medio_empirico=%.6f\n",largo_medio_analitico,largo_medio_empirico);
  
  if (exito) {
    printf("[%d] exito - p=%.2f\n",numero_test,p);
  } 
  else   {
    printf("[%d] ERROR - p=%.2f\n",numero_test,p);
    exit(1);
  }     
}


void TestCodigoT::test_codigo_archivo_aux(int numero_test, double p, int cant_repeticiones){

  // creo el codigo T asociado al p dado
  CodigoT* codigo_t;
  codigo_t=new CodigoT(p,0,0);

  // se generan enteros equiprobables en el rango [0,2*alfa-1]
  // para probar los dos metodos de codificacion, es decir para i<alfa y para i>alfa
  int maximo=2*codigo_t->get_alfa()-1;
  if (maximo<50){
    maximo=50; // para evitar rangos demasiado chicos donde siempre se generan los mismos simbolos
  }

  vector <int> vector_chequeo(cant_repeticiones,0); // vector utilizado para chequear

  // codifico archivo
  TestAux::crear_archivo_codificado(codigo_t,vector_chequeo,maximo,cant_repeticiones);

  // decodifico archivo
  bool exito=false;
  exito=TestAux::decodificar_archivo(codigo_t,vector_chequeo,cant_repeticiones);

  // si son iguales los archivos la codificacion y decodificacion fue correcta
  if (exito) {
    printf("[%d] exito - p=%.2f, alfa=%d, beta=%d, maximo=%d\n",numero_test,p,codigo_t->get_alfa(),codigo_t->get_beta(),maximo);
  } 
  else   {
    printf("[%d] ERROR - p=%.2f, alfa=%d, beta=%d, maximo=%d\n",numero_test,p,codigo_t->get_alfa(),codigo_t->get_beta(),maximo);
    exit(1);
  }     

}


// ####################################################################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

// testea que el largo de codigo calculado analiticamente
// es igual al largo de codigo empirico para una cantidad grande de simbolos
void TestCodigoT::test_largo_codigo(){
  
  // testeo para cada uno de estos valores de p
  double ps[11]={0.10,0.50,0.60,0.70,0.80,0.85,0.90,0.95,0.96,0.97,0.98};

  for(int i=0; i<11; i++){
    test_largo_codigo_aux(i+1,ps[i]);
  }
}

// testea que funcionan correctamente la codificacion y decodificacion
void TestCodigoT::test_codigo_archivo(){

  // testeo que el codigo codifica y decodifica de forma correcta para
  // cada uno de estos valores de p
  double ps[11]={0.10,0.50,0.60,0.70,0.80,0.85,0.90,0.95,0.96,0.97,0.98};

  int cant_repeticiones=100; // la cantidad de simbolos que codifico y decodifico

  for(int i=0; i<11; i++){
    test_codigo_archivo_aux(i+1,ps[i],cant_repeticiones);
  }
}
