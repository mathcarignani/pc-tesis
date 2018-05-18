#ifndef __FILE_UTILS_H__
#define __FILE_UTILS_H__

#include <cstdio>
#include <cstdlib>
#include <string>
#include "bit_stream.h"

class FileUtils {

public:

 	// Compares two files, returns 0 if they match.
  // Otherwise it returns the index of the first different bit.
  static int compare(char* file1, char* file2);

  // Writes unary coding of integer n in the file.
  static void unary_code(BitStreamWriter* file, int n);

  // Returns the unary decode of the next integer in the file.
  // It returns -1 if the file reaches its end before decoding.
  static int unary_decode(BitStreamReader* file);

};

#endif