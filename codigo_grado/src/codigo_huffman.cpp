#include "codigo_huffman.h"
using namespace std;

int CodigoHuffman::get_cantidad_simbolos(){
  return cantidad_simbolos;
}
ArbolCodigo* CodigoHuffman::get_arbol_codigo(){
  return arbol_codigo;
}
vector <PalabraDeCodigo*> CodigoHuffman::get_vector_codigo(){
  return vector_codigo;
}
vector <double> CodigoHuffman::get_probabilidades(){
  return probabilidades;
}
Distribucion* CodigoHuffman::get_distribucion(){
  return distribucion;
}

// ####################################################################################################### //
// ################################### private static #################################################### //
// ####################################################################################################### //

void CodigoHuffman::obtener_dos_probabilidades_menores(vector <Nodo*> huffman,
                                                        int cant_simbolos,
                                                        int & menor_indice_menor,
                                                        int & mayor_indice_menor){
  if (huffman[0]->get_prob()<=huffman[1]->get_prob()){
    menor_indice_menor=0; mayor_indice_menor=1;
  }
  else{
    menor_indice_menor=1; mayor_indice_menor=0;
  }
  
  for (int j=2; j<cant_simbolos; j++){
    double prob_actual=huffman[j]->get_prob();

    if (prob_actual<huffman[mayor_indice_menor]->get_prob()){ // j pasa a ser uno de los dos menores
      if (prob_actual<huffman[menor_indice_menor]->get_prob()){ // j pasa a ser el menor de los dos menores
        // si los dos menores eran iguales me fijo que quede el de menor indice, el otro lo sustituyo por j
        if (huffman[menor_indice_menor]->get_prob()==huffman[mayor_indice_menor]->get_prob()){
          menor_indice_menor= (mayor_indice_menor<mayor_indice_menor) ? mayor_indice_menor : menor_indice_menor;
        }
        mayor_indice_menor=menor_indice_menor;
        menor_indice_menor=j;
      }
      else { // j pasa a ser el mayor de los dos menores
        mayor_indice_menor=j;
      }
    }
  }

  // ya tengo los dos menores, ahora hago que menor_indice_menor sea menor a mayor_indice_menor
  if (menor_indice_menor>mayor_indice_menor){ 
    int temp=menor_indice_menor;
    menor_indice_menor=mayor_indice_menor;
    mayor_indice_menor=temp;
  }
}

vector <Nodo*> CodigoHuffman::crear_hojas(){
  Nodo* nodo;
  vector <Nodo*> hojas(cantidad_simbolos,nodo);

  if (distribucion==NULL){
    for (int i=0; i<cantidad_simbolos; i++){
      nodo=new Nodo(i,probabilidades[i]); // nodo hoja
      hojas[i]=nodo;
    }
  }
  else {
    for (int i=0; i<cantidad_simbolos; i++){
      nodo=new Nodo(i,distribucion->prob(i)); // nodo hoja
      hojas[i]=nodo;
    }
  }
  return hojas;
}

// Dado un vector de 'cant_simbolos' probabilidades, devuelve
//   el arbol asociado al codigo de huffman para esas probabilidades
//   donde sus 'cant_simbolos' hojas estan asociadas a una palabra de codigo.
// >> retorna la raiz del arbol
// >> este procedimiento se utiliza al DECODIFICAR
ArbolCodigo* CodigoHuffman::calcular_arbol(vector <Nodo*> huffman, int cant_simbolos){
  Nodo* nodo;

  // Cada iteracion es un paso del algoritmo de huffman
  //  donde termino sumando dos probabilidades
  for (int i=0; i<cant_simbolos-1; i++){

    // obtengo las dos menores probabilidades
    int menor_indice_menor,mayor_indice_menor;
    obtener_dos_probabilidades_menores(huffman,cant_simbolos,menor_indice_menor,mayor_indice_menor);

    // creo un nodo que suma las probabilidades
    nodo=new Nodo(huffman[menor_indice_menor],huffman[mayor_indice_menor]); // nodo no hoja
    huffman[menor_indice_menor]=nodo;

    // anulo esta entrada
    huffman[mayor_indice_menor]->set_prob(2);
  }
  
  // creo y devuelvo un arbol igual al nodo raiz
  ArbolCodigo* arbol_codigo;
  arbol_codigo=new ArbolCodigo(huffman[0]);

  return arbol_codigo;
}

// Dado un arbol de huffman, calculado en el procedimiento anterior,
//   devuelve un vector con las 'cant_simbolos' palabras de codigo
//   donde cada palabra de codigo esta asociada a una hoja del arbol de huffman.
// >> este procedimiento se utiliza al CODIFICAR
vector <PalabraDeCodigo*> CodigoHuffman::calcular_codigo_de_arbol(ArbolCodigo* arbol_codigo,
                                                                  int cant_simbolos,
                                                                  bool solo_largos){
  
  // en este vector se guardan las palabras de codigo
  PalabraDeCodigo* palabra;
  vector <PalabraDeCodigo*> codigo_huffman(cant_simbolos,palabra);
  
  vector <bool> entero;
  if (solo_largos){
    arbol_a_codigo_solo_largos(arbol_codigo->get_raiz(),0,entero,codigo_huffman);
  }
  else {
    arbol_a_codigo(arbol_codigo->get_raiz(),0,entero,codigo_huffman);
  }

  return codigo_huffman;
}

// Procedimiento recursivo que llena el vector codigo con las palabras de codigo
//   correspondientes a las hojas del arbol de huffman
void CodigoHuffman::arbol_a_codigo(Nodo* nodo,
                                   int largo,
                                   vector <bool> entero,
                                   vector <PalabraDeCodigo*> & codigo){

  // si el nodo es una hoja le seteo palabra_entero y palabra_largo
  // y termina la recursion
  if (nodo->nodo_es_hoja()){
    PalabraDeCodigo* palabra=new PalabraDeCodigo(largo,entero);
    codigo[nodo->get_entero()]=palabra;
  }
  // si el nodo no es una hoja sigo recorriendo el arbol hacia abajo
  // (llamando a este mismo procedimiento para cada hijo)
  else {
    largo++;

    // agrego un cero a la derecha
    entero.push_back(false);
    arbol_a_codigo(nodo->get_hijo_cero(),largo,entero,codigo);

    entero.pop_back(); // quito el cero de la derecha
    entero.push_back(true); // agrego un uno a la derecha
    arbol_a_codigo(nodo->get_hijo_uno(),largo,entero,codigo);
  }
}

// igual al procedimiento anterior pero solo importa el largo de las palabras
void CodigoHuffman::arbol_a_codigo_solo_largos(Nodo* nodo,
                                               int largo,
                                               vector <bool> entero,
                                               vector <PalabraDeCodigo*> & codigo){

  // si el nodo es una hoja le seteo palabra_entero y palabra_largo
  // y termina la recursion
  if (nodo->nodo_es_hoja()){
    PalabraDeCodigo* palabra=new PalabraDeCodigo(largo);
    codigo[nodo->get_entero()]=palabra;
  }
  // si el nodo no es una hoja sigo recorriendo el arbol hacia abajo
  // (llamando a este mismo procedimiento para cada hijo)
  else {
    largo++;
    arbol_a_codigo_solo_largos(nodo->get_hijo_cero(),largo,entero,codigo);
    arbol_a_codigo_solo_largos(nodo->get_hijo_uno(),largo,entero,codigo);
  }
}

// ####################################################################################################### //
// ########################################### creadores ################################################# //
// ####################################################################################################### //

// opcion 1 - se crea el codigo a partir de un vector de probabilidades
//             (cuyo largo es mayor o igual a cantidad_simbolos)
CodigoHuffman::CodigoHuffman(int cant_simbolos,
                             vector <double> probabilidades_,
                             bool solo_arbol,
                             bool solo_largos){

  cantidad_simbolos=cant_simbolos;
  probabilidades=probabilidades_;
  distribucion=NULL;

  vector <Nodo*> hojas=crear_hojas();
  arbol_codigo=calcular_arbol(hojas,cant_simbolos);

  if (!solo_arbol){
    vector_codigo=calcular_codigo_de_arbol(arbol_codigo,cant_simbolos,solo_largos);
  }
}

// opcion 2 - se crea el codigo a partir de una instancia de Distribucion
CodigoHuffman::CodigoHuffman(int cant_simbolos,
                             Distribucion* distribucion_,
                             bool solo_arbol,
                             bool solo_largos){
  
  cantidad_simbolos=cant_simbolos;
  distribucion=distribucion_;

  vector <Nodo*> hojas=crear_hojas();
  arbol_codigo=calcular_arbol(hojas,cant_simbolos);

  if (!solo_arbol){
    vector_codigo=calcular_codigo_de_arbol(arbol_codigo,cant_simbolos,solo_largos);
  }
}


// ####################################################################################################### //
// ####################################################################################################### //
// ######################################## codigo.h ##################################################### //
// ####################################################################################################### //
// ####################################################################################################### //

// imprime la informacion que define al codigo en pantalla
void CodigoHuffman::mostrar_codigo(){
  if (distribucion!=NULL){
    printf(" Codigo Huffman para una distribucion");
    if (distribucion->es_BN()) printf(" binomial negativa ");
    else                        printf(" geometrica ");

    printf("con parametro p=%.2f",distribucion->get_p());
    printf("\n");
    imprimir_columnas();
      
    for (int i=0; i<cantidad_simbolos; i++){
      imprimir_probabilidad(i,distribucion->prob(i));
    }
    printf("\n");
  }
}

// Calcula el largo medio teniendo en cuenta una distribucion que depende del codigo:
// [1] para un codigo de huffman tiene en cuenta las probabilidades a partir de las cuales fue creado
double CodigoHuffman::largo_medio(){
  double largo_medio=0;
  if (distribucion!=NULL){
    for(int i=0; i<cantidad_simbolos; i++){
      largo_medio+=distribucion->prob(i)*codificar_simbolo_largo(i);
    }
  }
  else {
    for(int i=0; i<cantidad_simbolos; i++){
      largo_medio+=probabilidades[i]*codificar_simbolo_largo(i);
    }
  }
  return largo_medio;
}

// devuelve true sii los codigos son iguales (largo y palabra de codigo)
bool CodigoHuffman::comparar_codigos(Codigo* codigo){
  bool iguales=arbol_codigo->arbol_es_igual(((CodigoHuffman*)codigo)->get_arbol_codigo());
  return iguales;
}

// devuelve la palabra de codigo con la que se codifica un simbolo
// si unario>=0 entonces se concatena el codigo unario 
// si se concatena el codigo unario el booleano indica si va antes o despues
PalabraDeCodigo* CodigoHuffman::codificar_simbolo(int simbolo, int & unario, bool & antes){
  unario=-1;
  antes=false;
  return vector_codigo[simbolo];
}

// devuelve el largo de la palabra de codigo con que se codifica un simbolo
int CodigoHuffman::codificar_simbolo_largo(int simbolo){
  return vector_codigo[simbolo]->get_largo();
}

// imprime en pantalla la palabra de codigo con la que se codifica un simbolo
void CodigoHuffman::codificar_simbolo_imprimir(int simbolo, int espacios_antes, int largo_total){
  vector_codigo[simbolo]->imprimir_palabra_espacios(espacios_antes,largo_total);
}

// decodifica el proximo simbolo leyendo del archivo
// (devuelve -1 si termina el archivo antes)
int CodigoHuffman::decodificar_simbolo_archivo(BitStreamReader* archivo){
  // http://stackoverflow.com/questions/1486904/how-do-i-best-silence-a-warning-about-unused-variables
  (void) archivo;
  return 0;
}
