#include "codigo_golomb.h"
using namespace std;

int CodigoGolomb::get_l(){
  return l;
}
double CodigoGolomb::get_p(){
  return p;
}
ArbolCodigo* CodigoGolomb::get_arbol_codigo(){
  return arbol_codigo;
}
vector <PalabraDeCodigo*> CodigoGolomb::get_vector_codigo(){
  return vector_codigo;
}

// ####################################################################################################### //
// ######################################## static private ############################################### //
// ####################################################################################################### //

// Calcula k y acc=2**k a partir de l
// k es el minimo entero tal que acc=2**k>=l, es decir k=ceil(log2(l))
// Ejs. l={1,2,3,4,5,...} => acc={1,2,4,4,8,...} => k={0,1,2,2,3,...}
void CodigoGolomb::calcular_k_y_acc(int l, int &k, int &acc){
  k=0; 
  acc=1;
  while (acc<l){
    k++;
    acc*=2;
  }
}

Nodo* CodigoGolomb::crear_arbol_golomb(int hojas, int largo, vector <bool> entero,
                                        vector <PalabraDeCodigo*> & codigo, int & indice_codigo){
  Nodo* nodo;

  // el nodo es una hoja
  if (hojas==1){

    // agrego la palabra al vector del codigo
    PalabraDeCodigo* palabra=new PalabraDeCodigo(largo,entero);
    codigo[indice_codigo]=palabra;

    nodo=new Nodo(indice_codigo, 0); // prob=0, no importa

    indice_codigo++;
  }
  else { // el nodo no es una hoja
    largo++;

    int hojas_cero;
    int hojas_uno;

    // acc es la maxima cantidad de hojas posible en el ultimo nivel
    // si hojas==2 -> acc==2
    // si hojas>2 --> acc>=4
    int k=0;
    int acc=0;
    calcular_k_y_acc(hojas,k,acc);

    // l=acc=2**k, el arbol es completo
    if (acc==hojas){
      hojas_cero=acc/2;
      hojas_uno=acc/2;
    }
    else { // acc=2**k > l, el arbol tiene mas hojas en el hijo uno (no es completo)

      // cantidad de nodos del penultimo nivel (>=2, porque acc>=4, porque hojas>2)
      int nodos_penultimo=acc/2;

      // cantidad de nodos del penultimo nivel que son hojas
      int nodos_hojas=acc-hojas;

      // el subarbol del hijo cero es completo hasta el penultimo nivel del arbol
      // el subarbol del hijo uno tiene hojas en el ultimo nivel (puede ser completo)
      if (nodos_hojas>=nodos_penultimo/2){
        hojas_cero=nodos_penultimo/2;
        hojas_uno=hojas-hojas_cero;
      }
      // el subarbol del hijo uno es completo hasta el ultimo nivel
      // el subarbol del hijo cero tiene hojas en el ultimo nivel (no es completo)
      else {
        hojas_uno=acc/2;
        hojas_cero=hojas-hojas_uno;
      }
    }

    // agrego un cero a la derecha
    entero.push_back(false);
    Nodo* hijo_cero=crear_arbol_golomb(hojas_cero,largo,entero,codigo,indice_codigo);

    entero.pop_back(); // quito el cero de la derecha
    entero.push_back(true); // agrego un uno a la derecha
    Nodo* hijo_uno=crear_arbol_golomb(hojas_uno,largo,entero,codigo,indice_codigo);

    nodo=new Nodo(hijo_cero,hijo_uno);
  }

  return nodo;
}

// ####################################################################################################### //
// ######################################## static public ################################################ //
// ####################################################################################################### //

// Dado p in (0,1) retorna el (único) l tal que p**l + p**(l+1) <= 1 < p**l + p**(l-1)
int CodigoGolomb::calcular_l(double p){
  
  int l=1;
  double inf=pow(p,l) + pow(p,l+1);
  double sup=pow(p,l) + pow(p,l-1);

  while ( (inf>1) || (1>=sup) ){
    l++;
    inf=pow(p,l) + pow(p,l+1);
    sup=pow(p,l) + pow(p,l-1);
  }

  return l;
}

// Para un l dado calcula todo el rango de p's para los que se cumple p**l + p**(l+1) <= 1 < p**l + p**(l-1)
// Nota1: el p de entrada debe cumplir p**l + p**(l+1) <= 1 < p**l + p**(l-1)
// Nota2: error=delta
void CodigoGolomb::calcular_rango_p(int l, double p, double &p_inf, double &p_sup){

  double delta=0.00000001;
  
  if (l==1){
    p_inf=0;
    p_sup=0.618034;
  }
  else {
    
    p_inf=p;
    while (calcular_l(p_inf)==l){
      p_inf-=delta;
    }
    p_inf+=delta; // p_inf esta adentro del rango
  
    p_sup=p;
    while (calcular_l(p_sup)==l){
      p_sup+=delta;
    }
    p_sup-=delta; // p_sup esta adentro del rango
  }
}

// ####################################################################################################### //
// ########################################### public #################################################### //
// ####################################################################################################### //

CodigoGolomb::CodigoGolomb(int l_, double p_, bool gpo2_, int k_){
  
  // si lo llamo desde el CodigoGolombBN
  if (gpo2_){ 
    l=l_;
    p=-1; // no importa
    gpo2=true;
    k=k_;
    return;
  }

  // si lo llamo en cualquier otro caso
  gpo2=false;
  k=-1; // no importa

  // obtengo o seteo el parametro l
  if (l_==0){
    p=p_;
    l=calcular_l(p_);
  }
  else {
    p=-1;
    l=l_;    
  }

  // si l!=1 tengo que calcular el arbol de huffman y el vector correspondiente
  if (l!=1){
    int hojas=l;
    int indice_codigo=0;
    PalabraDeCodigo* palabra;
    vector <PalabraDeCodigo*> codigo(l,palabra);

    vector <bool> entero;
    Nodo* raiz=crear_arbol_golomb(hojas,0,entero,codigo,indice_codigo);
    arbol_codigo=new ArbolCodigo(raiz);
    vector_codigo=codigo;
  }
}

// auxiliar de CodigoGolomb::mostrar_codigo()
// tambien utilizado en CodigoGolombBN::mostrar_codigo()
void CodigoGolomb::mostrar_aux(){
  if (l!=1){
    printf(" indice    |  palabra de codigo  \n");
    printf("---------------------------------\n");
    for(int i=0; i<l; i++){
      Impresion::imprimir_int(i,3,8);
      printf("|");
      PalabraDeCodigo* palabra=vector_codigo[i];
      palabra->imprimir_palabra_espacios(2,0);
      printf("\n");
    }
  }
}

// wrapper para distinguir casos cuando gpo2 es true y false
PalabraDeCodigo* CodigoGolomb::obtener_palabra(int i){
  if (gpo2){
    bool a=true; // dummys
    int unario=0;
    return codificar_simbolo(i, unario, a); // va a tener un 0 adelante
  }
  else {
    return vector_codigo[i];
  }
}

// ####################################################################################################### //
// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

// imprime la informacion que define al codigo en pantalla
void CodigoGolomb::mostrar_codigo(){
  printf(" Codigo Golomb con l=%d",l);
  if (p!=-1){
    printf(" (calculado para p=%.2f)",p);
  }  
  printf("\n");
  printf("---------------------------------\n");
  mostrar_aux();
  printf("\n");
}
  
// Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
// [2] para un codigo de golomb tiene en cuenta una distribucion geometrica
double CodigoGolomb::largo_medio(){
  double largo_medio;

  int k, acc;
  calcular_k_y_acc(l,k,acc);

  largo_medio=CuentasCodigo::calcular_largo_medio_golomb_geometrica(p,l,k,acc);

  return largo_medio;
}

// devuelve true sii los codigos son iguales (largo y palabra de codigo)
bool CodigoGolomb::comparar_codigos(Codigo* codigo){

  bool iguales=(l==((CodigoGolomb*)codigo)->get_l());

  // asumo que los codigos que comparo tienen igual el valor de gpo2
  if (gpo2){
    return iguales;
  }

  iguales=iguales && (arbol_codigo->arbol_es_igual(((CodigoGolomb*)codigo)->get_arbol_codigo()));
  return iguales;
}

// devuelve la palabra de codigo con la que se codifica un simbolo
// si unario>=0 entonces se concatena el codigo unario 
// si se concatena el codigo unario el booleano indica si va antes o despues
PalabraDeCodigo* CodigoGolomb::codificar_simbolo(int simbolo, int & unario, bool & antes){
  
  antes=true; // en este codigo el unario va a la izquierda

  if (l==1){
    unario=simbolo;
    return NULL;
  }
  else { // parte unaria y codigo de huffman
    div_t div_res=div(simbolo,l); // simbolo= l*div_res.quot + div_res.rem

    unario=div_res.quot;

    if (gpo2){
      PalabraDeCodigo* palabra= new PalabraDeCodigo(k,div_res.rem);
      return palabra;
    }
    else {
      return (vector_codigo[div_res.rem]);
    }
  }
}

// devuelve el largo de la palabra de codigo con que se codifica un simbolo
int CodigoGolomb::codificar_simbolo_largo(int simbolo){
  int largo;
  largo=simbolo+1; // si l==1 solo hay parte unaria

  if (l>1) { // parte unaria y codigo de huffman
    div_t div_res=div(simbolo,l); // simbolo= l*div_res.quot + div_res.rem
    if (gpo2){
      largo=(div_res.quot+1)+k;
    }
    else{
      largo=(div_res.quot+1)+vector_codigo[div_res.rem]->get_largo();
    }
  }
  return largo;
}

// imprime en pantalla la palabra de codigo con la que se codifica un simbolo
void CodigoGolomb::codificar_simbolo_imprimir(int simbolo, int espacios_antes, int largo_total){

  if (l==1){
    PalabraDeCodigo::imprimir_palabra_unario(NULL,simbolo,true,espacios_antes,largo_total);
  }
  else {// parte unaria y codigo de huffman
    div_t div_res=div(simbolo,l); // simbolo= l*div_res.quot + div_res.rem

    PalabraDeCodigo* palabra=NULL;
    if (gpo2){
      palabra= new PalabraDeCodigo(k,div_res.rem);
    }
    else {
      palabra = vector_codigo[div_res.rem];
    }
    PalabraDeCodigo::imprimir_palabra_unario(palabra, // palabra
                                             div_res.quot, // unario
                                             true, // va antes la palabra y despues el unario
                                             espacios_antes, largo_total);
  }
}

// decodifica el proximo simbolo leyendo del archivo
// (devuelve -1 si termina el archivo antes)
int CodigoGolomb::decodificar_simbolo_archivo(BitStreamReader* archivo){
 
  //[SIEMPRE OCURRE] tiene parte unaria
  int unario=Archivo::decodificar_unario(archivo);

  // si unario==-1 se llego al fin del archivo
  if (unario==-1){
    return -1;
  }

 int entero_huffman=0;

  // if (alfa+beta>1){
  if (l>1){

    if (gpo2){ 
      int k_restante = k; // tengo que leer k bits

      while (k_restante>0){
        // me fijo si termino el archivo
        if (archivo->reachedEOF()){
          return -1;
        }
         
        // leo bit y bajo por el arbol
        if (archivo->getBit()){
          entero_huffman += pow(2,k_restante-1);
        }
        k_restante--;
      }
    }
    else {
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

       //[NUNCA OCURRE] no tiene parte unaria
       //if (entero_huffman<alfa){
       //  return entero_huffman;
       //}
     }  
  }

  int simbolo=entero_huffman+l*unario;
  return simbolo;
}
