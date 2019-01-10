#include "codigo_golomb_bn.h"
using namespace std;

CodigoGolomb* CodigoGolombBN::get_codigo_golomb(){
  return codigo_golomb;
}
double CodigoGolombBN::get_p(){
  return p;
}
int CodigoGolombBN::get_l(){
  return codigo_golomb->get_l();
}
int CodigoGolombBN::get_lambda(){
  return lambda;
}
vector <unsigned int> CodigoGolombBN::get_vector_perm(){
  return vector_perm;
}
vector <unsigned int> CodigoGolombBN::get_vector_perm_inverso(){
  return vector_perm_inverso;
}
double CodigoGolombBN::get_esperanza(){
  return esperanza;
}

// calcula la esperanza practica teniendo en cuenta unicamente
// los simbolos en el rango [simbolo_inicial,simbolo_final]
double CodigoGolombBN::calcular_esperanza_practica(int simbolo_inicial, int simbolo_final){

  int i_permutado;
  double esperanza__=0;
  for(int i=simbolo_inicial; i<=simbolo_final; i++){

    i_permutado=i;
    if (i<lambda){
      i_permutado=vector_perm_inverso[i];
    }
    esperanza__+=i_permutado*distribucion_bn->prob(i);
    //printf("%d - ",i);
  }
  return esperanza__;
}

int CodigoGolombBN::calcular_k(){

  // (1.1) calculo la esperanza de los enteros [0,lambda-1], mapeados en el vector lambda
  double esperanza_cabeza=calcular_esperanza_practica(0,lambda-1);
  
  // (1.2) calculo la esperanza de los enteros [lambda,inf)
  double esperanza_cola=distribucion_bn->esperanza_analitica_cola(lambda);

  //printf("lambda = %d ",lambda);
  //printf("esperanza_cabeza=%.5f / esperanza_cola=%.5f",esperanza_cabeza,esperanza_cola);
  // (1.3) calcula la esperanza total
  esperanza = esperanza_cabeza+esperanza_cola;//-esperanza_cola;

  //printf("esperanza = %0.5f ",esperanza);
  // (2) obtengo el k optimo aplicando la formula (8) del paper
  double golden_ratio=(sqrt(5)+1)/2;

  double param1=log(golden_ratio-1)/log(esperanza/(esperanza+1));
  double param2=floor( log(param1)/log(2) );
  double param3=1+param2;

  int k=0;
  if (param3>0){
    k=param3;
  }

  return k;
}

CodigoGolombBN::CodigoGolombBN(int l, double p_){
  // seteo p
  p=p_;

  // creo una distribucion BN
  distribucion_bn=new DistribucionBN(p_);

  // a partir de la distribucion obtengo el vector lambda
  double i_prima;
  vector_perm=distribucion_bn->calcular_vector_perm(i_prima,lambda);
  vector_perm_inverso=distribucion_bn->calcular_vector_perm_inverso(vector_perm,lambda);

  int k=0;

  if (l==0){
    k=calcular_k();
  }

  l=pow(2,k);

  // creo un codigo de golomb para el l dado
  codigo_golomb=new CodigoGolomb(l,-1,true,k);
}


// ####################################################################################################### //
// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

// imprime la informacion que define al codigo en pantalla
void CodigoGolombBN::mostrar_codigo(){

  printf(" Codigo Golomb Mod con l=%d y p=%.2f // lambda=%d - i'=%.5f - f(0)=%.5f",
          codigo_golomb->get_l(),p,lambda,distribucion_bn->calcular_i_prima(),distribucion_bn->prob(0));
  printf("\n");
  // printf("---------------------------------\n");
  // codigo_golomb->mostrar_aux();
  // printf("---------------------------------\n");
  // printf(" indice    |  codigo golomb de   \n");
  // printf("---------------------------------\n");  
  // for (int i=0; i<lambda; i++){
  //   Impresion::imprimir_int(i,3,8);
  //   printf("|");
  //   Impresion::imprimir_int(vector_perm[i],2,0);
  //   if (vector_perm[i]==0){
  //     printf(" (+ probable)");
  //   }
  //   printf("\n");
  // }
  // printf("\n");  
}

// Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
// [3] para un codigo de golomb mod tiene en cuenta una distribucion binomial negativa
double CodigoGolombBN::largo_medio(){

  // calculo el largo medio empirico de los primeros lambda simbolos
  double largo_medio_cabeza=0;
  for(int i=0; i<lambda; i++){
    largo_medio_cabeza+=codificar_simbolo_largo(i)*distribucion_bn->prob(i);
  }

  // obtengo el l del codigo de golomb
  int l=codigo_golomb->get_l();

  // calculo el largo medio analitico de los l supersimbolos
  double largo_medio_cola=0;
  for (int i=lambda; i<lambda+l; i++){

    //int gamma=i-lambda; // gamma={0,1,..,l-1}
    double largo_simbolo=codificar_simbolo_largo(i);

    // aplico la misma formula que en el codigo t (con diferentes parametros)
    largo_medio_cola+=CuentasCodigo::calcular_largo_medio_supersimbolo(p,l,i,largo_simbolo-1);
  }

  //printf("largo_medio_cabeza=%.5f, largo_medio_cola=%.5f",largo_medio_cabeza,largo_medio_cola);
  double largo_medio=largo_medio_cabeza+largo_medio_cola;
  //printf("A=%.5f / B=%.5f",largo_medio_cabeza,largo_medio_cola);
  return largo_medio;
}

// devuelve true sii los codigos son iguales (largo y palabra de codigo)
bool CodigoGolombBN::comparar_codigos(Codigo* codigo){
  
  // comparo los enteros lambda
  bool iguales=(lambda==(((CodigoGolombBN*)codigo)->get_lambda()));

  // comparo los vectores lambda
  if (iguales){
    vector <unsigned int> vector_perm_2=((CodigoGolombBN*)codigo)->get_vector_perm();
    for (int i=0; i<lambda; i++){
      if (vector_perm[i]!=vector_perm_2[i]){
        iguales=false;
        break;
      }
    }
  }

  // comparo los codigos de golomb
  iguales=iguales && codigo_golomb->comparar_codigos(((CodigoGolombBN*)codigo)->get_codigo_golomb());

  return iguales;
}

// devuelve la palabra de codigo con la que se codifica un simbolo
// si unario>=0 entonces se concatena el codigo unario 
// si se concatena el codigo unario el booleano indica si va antes o despues
PalabraDeCodigo* CodigoGolombBN::codificar_simbolo(int simbolo, int & unario, bool & antes){

  int simbolo_mapeado=simbolo;

  // el simbolo se mapea utilizando el vector_perm
  if (simbolo_mapeado<lambda){
    simbolo_mapeado=vector_perm[simbolo];
  }

  PalabraDeCodigo* palabra;
  palabra=codigo_golomb->codificar_simbolo(simbolo_mapeado,unario,antes);

  return palabra;
}

// devuelve el largo de la palabra de codigo con que se codifica un simbolo
int CodigoGolombBN::codificar_simbolo_largo(int simbolo){
  int simbolo_mapeado=simbolo;
  if (simbolo<lambda){
    simbolo_mapeado=vector_perm[simbolo];
  }
  return codigo_golomb->codificar_simbolo_largo(simbolo_mapeado);
}

// imprime en pantalla la palabra de codigo con la que se codifica un simbolo
void CodigoGolombBN::codificar_simbolo_imprimir(int simbolo, int espacios_antes, int largo_total){
  int simbolo_mapeado=simbolo;
  if (simbolo<lambda){
    simbolo_mapeado=vector_perm[simbolo];
  }
  codigo_golomb->codificar_simbolo_imprimir(simbolo_mapeado,espacios_antes,largo_total);
}

// decodifica el proximo simbolo leyendo del archivo
// (devuelve -1 si termina el archivo antes)
int CodigoGolombBN::decodificar_simbolo_archivo(BitStreamReader* archivo){

  int simbolo_mapeado=codigo_golomb->decodificar_simbolo_archivo(archivo);
  if (simbolo_mapeado<lambda){
    simbolo_mapeado=vector_perm_inverso[simbolo_mapeado];
  }
  return simbolo_mapeado;
}
