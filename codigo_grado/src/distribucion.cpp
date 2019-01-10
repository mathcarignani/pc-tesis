#include "distribucion.h"
using namespace std;

// Esta funcion genera el vector de probabilidades de la distribucion,
//   acumulando en el simbolo entero_acc (cant_simbolos-1) las probabilidades
//  de los simbolos [entero_acc,infinito).
// Se realizan chequeos de error sobre la precision de los calculos.
// Se calcula la entropia empirica.
// PRECONDICION: cant_simbolos>1
vector <double> Distribucion::generar_vector(int & cant_simbolos, // entero_acc=cant_simbolos-1
                                             double & entropia_practica){
  // chequeo precondicion
  if (cant_simbolos<=1){
    printf("ERROR Distribucion::generar_vector. cant_simbolos=%d\n",cant_simbolos);
    exit(1);
  }

  // el vector puede tener hasta entero_acc + 1 simbolos
  // con una precision aceptable
  int entero_acc=calcular_largo_vector(cant_simbolos-1); 
                                                            
  if (entero_acc < cant_simbolos-1){
    cant_simbolos=entero_acc+1; // actualizo cant_simbolos
  }

  double acc=0; // voy haciendo la sumatoria para calcular la probabilidad del ultimo simbolo (entero_acc)
  double current;
  vector <double> probabilidades(cant_simbolos,0); 
  
  for (int i=0; i<entero_acc; i++){
    
    current=prob(i); // current=P(i)

    acc+=current;

    entropia_practica+=termino_entropia_practica(current); // actualizo la entropia empirica
    probabilidades[i]=current; // actualizo el vector de probabilidades
  }

  current=1-acc;

  entropia_practica+=termino_entropia_practica(current); // actualizo la entropia empirica
  probabilidades[entero_acc]=current; // actualizo el vector de probabilidades
    
  //printf("cant_simbolos=%d, entero_acc=%d, current=%.6f\n",cant_simbolos,entero_acc,current);
  return probabilidades;
}

// analogo a Distribucion::generar_vector pero sin el vector
double Distribucion::calcular_entropia_practica(int & cant_simbolos){

  double entropia_practica=0;
  
  // chequeo precondicion
  if (cant_simbolos<=1){
    printf("ERROR Distribucion::calcular_entropia_practica. cant_simbolos=%d\n",cant_simbolos);
    exit(1);
  }

  // el vector puede tener hasta entero_acc + 1 simbolos
  // con una precision aceptable
  int entero_acc=calcular_largo_vector(cant_simbolos-1); 
                                                            
  if (entero_acc < cant_simbolos-1){
    cant_simbolos=entero_acc+1; // actualizo cant_simbolos
  }

  double acc=0; // voy haciendo la sumatoria para calcular la probabilidad del ultimo simbolo (entero_acc)
  double current;
  //vector <double> probabilidades(cant_simbolos,0); 
  
  for (int i=0; i<entero_acc; i++){
    
    current=prob(i); // current=P(i)

    acc+=current;

    entropia_practica+=termino_entropia_practica(current); // actualizo la entropia empirica
    //probabilidades[i]=current; // actualizo el vector de probabilidades
  }

  current=1-acc;

  entropia_practica+=termino_entropia_practica(current); // actualizo la entropia empirica
  //probabilidades[entero_acc]=current; // actualizo el vector de probabilidades
    
  //printf("cant_simbolos=%d, entero_acc=%d, current=%.6f\n",cant_simbolos,entero_acc,current);
  return entropia_practica;
}

// Devuelve el minimo entero i tal que chequeo_precision(i-1,i,p)=false
// (es decir que i es el indice del entero en el que se acumula)
// Si no falla el chequeo de precision antes devuelve el mismo numero que entra
int Distribucion::calcular_largo_vector(int entero_acc){
  int i=-1;
  bool seguir=true;
  while (seguir){
    i++;
    seguir=( (i==0) || (i<entero_acc && chequeo_precision(i-1,i)) );
  }
  return i;
}

// Devuelve false si falla la precision (en ese caso se va acumular en el simbolo i_actual)
bool Distribucion::chequeo_precision(int i_anterior, int i_actual){

  // si p**i da 0 ya perdi demasiada precision
  if (pow(p,i_actual)<=0){
    return false;
  }

  // si fabs(p**i/p**(i-1) - p) > precision ya perdi demasiada precision
  if ( ( fabs( pow(p,i_actual)/pow(p,i_anterior) - p) ) > precision_ ){
    return false;
  }

  return true;
}

// Calcula un termino de la entropia empirica.
double Distribucion::termino_entropia_practica(double prob){
  double res;
  if (prob>0 && prob<1){
    res=-prob*( (log(prob))/log(2));
  }
  else{
    res=0;
  }  
  return res;
}
