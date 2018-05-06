
#include "operation_utils.h"

#include <math.h>

void OperationUtils::set_right_left(float n, int *left, int *right)
{
    (*left) = floor(n); // floor(23.55) = 23
    (*right) = (n - *left)*100;
}
