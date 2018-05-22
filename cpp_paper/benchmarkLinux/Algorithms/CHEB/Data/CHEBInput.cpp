#ifndef __CHEBINPUT_CPP
#define __CHEBINPUT_CPP

#include "CHEBInput.h"
#include "../../../stdafx.h"

CHEBInput::CHEBInput(void)
{
}

CHEBInput::CHEBInput(CDataStream *data, double esp)
{
	m_originalStream = data;
	m_dataLength = data->size();
	m_dEsp = esp;
}

CHEBInput::~CHEBInput(void)
{
}

int CHEBInput::getDataLength()
{
	return m_dataLength; 
}

double CHEBInput::getEsp()
{
	return m_dEsp * (m_originalStream->getMax() -  m_originalStream->getMin()); 
}

double CHEBInput::getMaxValue()
{
	return m_originalStream->getMax();
}
double CHEBInput::getMinValue()
{
	return m_originalStream->getMin();
}

// Purpose	: Get each window data from Raw data stream 									
// Parameter:	from  : the position need to get window data in raw data stream			
//				length: the size of window data											
double* CHEBInput::getWndData(int from, int length)
{
	int nTo = from + length;
	double *dWindData = (double*) (malloc(length * sizeof(double)));
	for(int i = 0; i < length; i++)
	{
		dWindData[i] = m_originalStream->getAt(i + from).value;
	}
	return dWindData;
}

#endif