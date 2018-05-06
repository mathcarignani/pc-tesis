#ifndef __APCAINPUT_H
#define __APCAINPUT_H

#pragma once

#include "../../../DataManagementLayer/Data/Input_SingleStreamAlg.h"

class APCAInput : public Input_SingleStreamAlg
{
public:
	APCAInput(CDataStream* rawData, double esp): Input_SingleStreamAlg(rawData, esp){}
};

#endif
