#ifndef __CHEBINPUT_H
#define __CHEBINPUT_H

#pragma once
#include "../../../DataManagementLayer/Data/DataStream.h"

class CHEBInput
{
private:
	CDataStream* m_originalStream;
	int m_dataLength;
	double m_dEsp;

public:
	CHEBInput(void);
	CHEBInput(CDataStream* data, double esp);
	~CHEBInput(void);

	int getDataLength();
	double getEsp();
	double getMaxValue();
	double getMinValue();

	// Get each window data from Raw data stream
	double* getWndData(int from, int length);
};

#endif
