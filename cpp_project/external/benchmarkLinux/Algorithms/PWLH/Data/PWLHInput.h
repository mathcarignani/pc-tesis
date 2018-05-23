#ifndef __PWLHINPUT_H
#define __PWLHINPUT_H

#pragma once
#include "../../../DataManagementLayer/Data/Input_SingleStreamAlg.h"

class PWLHInput : public Input_SingleStreamAlg
{
public:
	PWLHInput(CDataStream* rawData, double esp): Input_SingleStreamAlg(rawData, esp){}
};

#endif
