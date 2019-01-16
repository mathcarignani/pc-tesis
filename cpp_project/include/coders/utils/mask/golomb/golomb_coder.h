
#ifndef CPP_PROJECT_GOLOMB_CODER_H
#define CPP_PROJECT_GOLOMB_CODER_H

#include "coder_base.h"

class GolombCoder {

private:
    CoderBase* coder;
    double p; // success probability
    int l; // single integer which satisfies the equation: p**l + p**(l+1) <= 1 < p**l + p**(l-1)
    int k; // l=2**k

    static int calculateL(double p);
    static int nearestK(int & l);
    void codeRunLength(int length);

public:
    GolombCoder(CoderBase* coder_, double p_);
    void code(int column_index);

};

#endif //CPP_PROJECT_GOLOMB_CODER_H
