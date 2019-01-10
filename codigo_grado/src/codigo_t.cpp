#include "codigo_t.h"
using namespace std;

void CodigoT::calcular_alfa_y_beta(){
  int cant_simbolos=INT_MAX;

  // genero el vector de probabilidades de la distribucion BN
  // para la maxima cantidad de simbolos antes del error de precision
  DistribucionBN* distribucion_bn=new DistribucionBN(p);
  double entropia_practica=0;
  vector <double> probabilidades;
  probabilidades=distribucion_bn->generar_vector(cant_simbolos,entropia_practica);

  // creo un codigo de huffman a partir del vector de probabilidades
  // solo_largos = TRUE
  CodigoHuffman* codigo_huffman=new CodigoHuffman(cant_simbolos,probabilidades,false,true);
  vector <PalabraDeCodigo*> vector_huff=codigo_huffman->get_vector_codigo();

  // calculo el perfil del codigo de huffman
  Perfil* perfil=((Codigo*)codigo_huffman)->generar_perfil(cant_simbolos);
  
  //perfil->imprimir_perfil();
  
  // obtengo alfa y beta a partir del patron mas representativo del perfil
  //   del codigo de huffman
  Patron* mayor_patron=perfil->get_patrones()[perfil->get_indice_mayor_patron()];
  alfa=mayor_patron->get_primer_simbolo();
  beta=mayor_patron->get_cant_palabras_serie();
  //printf("alfa=%d , beta=%d\n",alfa,beta);
}

// Es similar al procedimiento generar_vector_probabilidades, las diferencias son que:
//   >> en este caso solo interesa la distribucion binomial negativa
//   >> no se realiza ningun chequeo de precision
//   >> no se calcula la entropia empirica
// PRE: se llamo antes al procedimiento generar_vector_probabilidades con cant_simbolos>alfa
vector <double> CodigoT::generar_vector_probabilidades_para_huffman(double p,
                                                                    int alfa,
                                                                    int beta){
  vector <double> probabilidades(alfa+beta,0); 
  DistribucionBN* distribucion_bn=new DistribucionBN(p);

  for (int i=0; i<alfa+beta; i++){
    
    if (i<alfa){
      // 0<=i<alfa (alfa simbolos)
      probabilidades[i]=distribucion_bn->prob(i);
    }
    else {
      // alfa<=i<alfa+beta (beta simbolos)
      probabilidades[i]=CuentasCodigo::calcular_probabilidad_supersimbolo(p, beta, i);
    }    

  }
  return probabilidades;
}

// bool chequeo_cct(double p, int cant_simbolos, int alfa, int beta){
//   bool chequeo=true;
//   if (cant_simbolos!=0){
//     if ( (p<=0) || (p>=1) ) chequeo=false;
//     if (cant_simbolos<10) chequeo=false;
//     if ( (alfa<0) || (alfa>cant_simbolos-1) ) chequeo=false;
//     if (beta<1) chequeo=false;
//   }
//   return chequeo;
// }

CodigoT::CodigoT(double p_, int alfa_, int beta_){

  // seteo p
  p=p_;

  // si no estan seteados calculo alfa y beta a partir de p
  if (alfa_==0 && beta_==0){ 
    calcular_alfa_y_beta();
  }
  else {
    alfa=alfa_;
    beta=beta_;
  }

  if (alfa+beta>1){
    // probabilidades_huffman es un vector de largo alfa+beta
    probabilidades_huffman=generar_vector_probabilidades_para_huffman(p,alfa,beta);

    // creo un codigo de huffman con arbol y vector
    CodigoHuffman* codigo_huffman=new CodigoHuffman(alfa+beta,probabilidades_huffman,false,false);

    arbol_codigo=codigo_huffman->get_arbol_codigo();
    vector_codigo=codigo_huffman->get_vector_codigo();
  }
  else {
    arbol_codigo=NULL;
  }
  
}  

int CodigoT::get_alfa(){
  return alfa;
}
int CodigoT::get_beta(){
  return beta;
}


// ####################################################################################################### //
// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

// imprime la informacion que define al codigo en pantalla
void CodigoT::mostrar_codigo(){
  printf(" Codigo T para p=%.2f, alfa=%d, beta=%d",p,alfa,beta);
  printf("\n");
  Codigo::imprimir_columnas();
    
  if (alfa+beta>1){
    for (int i=0; i<alfa+beta; i++){
      imprimir_probabilidad(i,probabilidades_huffman[i]);
      if (i==alfa-1){
        printf("-----------------------------------------------------------------\n");
        printf("          alfa=");Impresion::imprimir_int(alfa,0,13); printf("||"); 
        printf("          beta=%d\n",beta);
        printf("-----------------------------------------------------------------\n");
      }
    }
  }
  
  printf("\n");
}  

// Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
// [4] para el codigo T tiene en cuenta una distribucion binomial negativa
double CodigoT::largo_medio(){

  double res;

  if (alfa+beta>1){
    
    double largo_medio_cabeza=0;
    if (alfa>0){
      // largo medio de los primeros alfa simbolos
      //   (son los simbolos que se codifican con huffman directamente)
      largo_medio_cabeza=calcular_largo_medio(probabilidades_huffman,vector_codigo,0,alfa-1);
    }
    
    double largo_medio_cola=0;
    // largo medio de los simbolos [alfa,inf)
    //   (es igual a suma de los largos medios de los beta supersimbolos)
    for (int j=alfa; j<alfa+beta; j++){
      largo_medio_cola+=CuentasCodigo::calcular_largo_medio_supersimbolo(p,beta,j,vector_codigo[j]->get_largo());
    }

    res=largo_medio_cabeza+largo_medio_cola;
  }
  else {
    res=(p+1)/(1-p);
  }

  return res;
}

// devuelve true sii los codigos son iguales (largo y palabra de codigo)
bool CodigoT::comparar_codigos(Codigo* codigo){
  bool res=(((CodigoT*)codigo)==NULL);
  return res; // TODO
}

// devuelve la palabra de codigo con la que se codifica un simbolo
// si unario>=0 entonces se concatena el codigo unario 
// si se concatena el codigo unario el booleano indica si va antes o despues
PalabraDeCodigo* CodigoT::codificar_simbolo(int simbolo, int & unario, bool & antes){
  
  antes=false; // en este codigo el unario va a la derecha

  PalabraDeCodigo* parte_binaria;

  int i=simbolo;
  if (i<alfa){ 
    // codifico i con el codigo de huffman obtenido (no hay parte unaria)
    parte_binaria=vector_codigo[i];
    unario=-1;
  }
  else { // i>=alfa

    // sea i-alfa = beta*cociente + resto
    // codifico i concatenando estos dos codigos
    // (1) codigo de huffman de alfa+resto
    // (2) codigo unario de cociente

    div_t div_res=div(i-alfa,beta); // i-alfa = beta*cociente + resto

    if (alfa+beta>1){
      parte_binaria=vector_codigo[alfa+div_res.rem];
    }
    else {
      parte_binaria=NULL;
    }
    unario=div_res.quot;
  }

  return parte_binaria;
}

// devuelve el largo de la palabra de codigo con que se codifica un simbolo
int CodigoT::codificar_simbolo_largo(int simbolo){

  int largo;
  int i=simbolo;

  if (i<alfa){
    largo=vector_codigo[i]->get_largo();
  }
  else {
    div_t div_res=div(i-alfa,beta); // i-alfa = beta*cociente + resto

    if (alfa+beta>1){
      largo=(div_res.quot+1)+vector_codigo[alfa+div_res.rem]->get_largo();
    }
    else {
      largo=div_res.quot+1;
    }
    
  }

  return largo;
}

// imprime en pantalla la palabra de codigo con la que se codifica un simbolo
void CodigoT::codificar_simbolo_imprimir(int simbolo, int espacios_antes, int largo_total){

  int i=simbolo;
  if (i<alfa){
    vector_codigo[i]->imprimir_palabra_espacios(espacios_antes,largo_total);
  }
  else {
    div_t div_res=div(i-alfa,beta); // i-alfa = beta*cociente + resto

    if (alfa+beta>1){
      PalabraDeCodigo::imprimir_palabra_unario(vector_codigo[alfa+div_res.rem], // palabra
                                                div_res.quot, // unario
                                                false, // va antes la palabra y despues el unario
                                                espacios_antes,largo_total);
    }
    else {
      PalabraDeCodigo::imprimir_palabra_unario(NULL, // palabra
                                                div_res.quot, // unario
                                                false, // va antes la palabra y despues el unario
                                                espacios_antes,largo_total);
    }
    
  }

}


// decodifica el proximo simbolo leyendo del archivo
// (devuelve -1 si termina el archivo antes)
int CodigoT::decodificar_simbolo_archivo(BitStreamReader* archivo){

  int entero_huffman=0;

  if (alfa+beta>1){

    // decodifico la parte del codigo de huffman
    // (para esto voy bajando por el arbol hasta llegar a una hoja)
     Nodo* nodo=arbol_codigo->get_raiz();

     bool seguir=true;
     while (seguir){
       // me fijo si termino el archivo
       if (archivo->reachedEOF()){
         return -1;
       }
       else {
         // leo bit y bajo por el arbol
         nodo=(archivo->getBit()) ? nodo->get_hijo_uno() : nodo->get_hijo_cero();
         seguir=!nodo->nodo_es_hoja();
       }
     }
     entero_huffman=nodo->get_entero();

     // no tiene parte unaria
     if (entero_huffman<alfa){
       return entero_huffman;
     }
  }

  //tiene parte unaria
  int unario=Archivo::decodificar_unario(archivo);

  // si unario==-1 se llego al fin del archivo
  if (unario==-1){
    return -1;
  }
  else {
    int simbolo=entero_huffman+beta*unario;
    return simbolo;
  }
}
