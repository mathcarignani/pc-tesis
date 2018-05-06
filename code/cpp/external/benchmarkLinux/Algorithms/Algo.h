#ifndef __ALGO_H
#define __ALGO_H

#include "../DataManagementLayer/Data/Output.h"

class Algo
{
    public:
            virtual ~Algo(void){}

                virtual Output* getOutput()=0;
                    virtual void compress()=0;
};

#endif

