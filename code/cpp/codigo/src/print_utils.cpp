#include "print_utils.h"

int PrintUtils::figure_count(double n){

  int figures=1;
  int ten_power=10; // 10**figure

  while (n>=ten_power){
    figures++;
    ten_power*=10;
  }
  return ten_power;
}

void PrintUtils::print_spaces(int n){
  if (n>0){
    for (int i=0; i<n; i++)
      printf(" ");
  }  
}

void PrintUtils::print_int(int n, int spaces_before, int total_length){
  
  print_spaces(spaces_before);
  
  printf("%d",n);
  
  int spaces_after=total_length-figure_count(n);
  print_spaces(spaces_after);
}

void PrintUtils::print_double(double n, int decimals_count, int spaces_before, int total_length){

  print_spaces(spaces_before);
  
  printf("%.*f",decimals_count,n);

  int double_length=figure_count(n)+1+decimals_count; // 1 for comma
  int spaces_after=total_length-double_length;
  print_spaces(spaces_after);
}
