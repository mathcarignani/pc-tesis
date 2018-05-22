#ifndef __PCAINPUT_H
#define __PCAINPUT_H

#include "../../../DataManagementLayer/Data/Input_SingleStreamAlg.h"

class PCAInput: public Input_SingleStreamAlg
{
private:
	int m_nWndSize;

public:
	PCAInput(CDataStream* rawData, int wndSize, double esp);

	int   getWndSize();

	// Get 'm_nWndSize' values which start from 'from' position
	void  getWndData(int from, double* wndData);
};

#endif
