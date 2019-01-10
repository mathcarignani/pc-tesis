#include "test_aux.h"
using namespace std;

vector <PalabraDeCodigo*> TestAux::crear_codigo(int enteros[], int largos[], 
                                                          int cant_simbolos){
  vector <PalabraDeCodigo*> codigo;

  for (int i=0; i<cant_simbolos; i++){
    PalabraDeCodigo* palabra=new PalabraDeCodigo(largos[i],enteros[i]);
    codigo.push_back(palabra);
  }
  return codigo;
}

double TestAux::calcular_largo_medio_empirico(Codigo* codigo, Distribucion* distribucion){
  
  int cant_simbolos=INT_MAX; // para obtener el maximo posible entero posible donde se mantiene la precision
  distribucion->calcular_entropia_practica(cant_simbolos);

  //printf("cant_simbolos=%d\n",cant_simbolos);

  // creo una clase distribucion para calcular el largo medio empirico
  ClaseCodigoDistribucion* clase_codigo_distribucion;
  clase_codigo_distribucion=new ClaseCodigoDistribucion(codigo,distribucion);

  double largo_medio_empirico;
  largo_medio_empirico=clase_codigo_distribucion->calcular_largo_medio(0,cant_simbolos);

  return largo_medio_empirico;
}

// ####################################################################################################### //
// ################# auxiliares para testear codificadores / decodificadores con archivos ################ //
// ####################################################################################################### //

// genera un numero aleatorio entre min y max inclusive
int TestAux::generar_numero_aleatorio(int min, int max){
  int res;
  //res=min + (rand() % (int)(max - min + 1));
  res=min + rand() % max;
  return res;
}

// crea un archivo donde los simbolos estan codificados con el codigo T
void TestAux::crear_archivo_codificado(Codigo* codigo,
                                       vector <int> & vector_chequeo,
                                       int maximo,
                                       int cant_repeticiones){
  
  srand(time(NULL)); // inicializa seed para rand()

  BitStreamWriter* archivo_codificado;
  archivo_codificado=new BitStreamWriter((char*)"archivo_codificado");

  int simbolo;
  for (int i=0; i<cant_repeticiones; i++){

    // genero un simbolo aleatorio
    simbolo=generar_numero_aleatorio(0,maximo);

    //printf("simbolo codificado %d --> %d\n",i,simbolo);

    // lo guardo en el vector de chequeo
    vector_chequeo[i]=simbolo;

    // lo codifico en el archivo
    codigo->codificar_simbolo_archivo(simbolo,archivo_codificado);
  }

  delete archivo_codificado;
}

// decodifico el archivo creado en el procedimiento anterior y 
//   voy chequeando su correctitud para cada simbolo
// devuelve true sii todos los simbolos fueron decodificados correctamente
bool TestAux::decodificar_archivo(Codigo* codigo,
                                  vector <int> vector_chequeo,
                                  int cant_repeticiones){
  BitStreamReader* archivo_codificado;
  archivo_codificado=new BitStreamReader((char*)"archivo_codificado");

  bool exito=true;
  int simbolo;
  for (int i=0; i<cant_repeticiones; i++){
    // decodifico el proximo simbolo del archivo
    simbolo=codigo->decodificar_simbolo_archivo(archivo_codificado);

    //printf("simbolo decodificado %d --> %d\n",i,simbolo);

    // si el simbolo decodificado no es correcto o si termino el archivo
    //   termino la ejecucion y devuelvo false
    if (simbolo!=vector_chequeo[i]){
      exito=false;
      break;
    }
  }

  delete archivo_codificado;

  return exito;
}
