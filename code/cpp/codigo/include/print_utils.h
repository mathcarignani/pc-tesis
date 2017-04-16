#ifndef __PRINT_UTILS_H__
#define __PRINT_UTILS_H__

#include <math.h>
#include <stdio.h>
#include <vector>

class PrintUtils {

public:

  // Returns the number of figures that a double has left of the comma.
  static int figure_count(double num);

  // If n>0 it prints n spaces, otherwise it doesn't print anything.
  static void print_spaces(int n);

  static void print_int(int n, int spaces_before, int total_length);

  static void print_double(double n, int decimals_count, int spaces_before, int total_length);

};

#endif
