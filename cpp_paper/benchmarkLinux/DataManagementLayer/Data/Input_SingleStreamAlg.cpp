#ifndef __INPUT_SINGLESTREAM_CPP
#define __INPUT_SINGLESTREAM_CPP

#include "Input_SingleStreamAlg.h"

Input_SingleStreamAlg::Input_SingleStreamAlg(CDataStream* rawData, double esp)
{
	m_pRawData = rawData;
	m_dEsp = (rawData->getMax() - rawData->getMin()) * esp;
}

double Input_SingleStreamAlg::getMinValue()
{
	return m_pRawData->getMin();
}

double Input_SingleStreamAlg::getMaxValue()
{
	return m_pRawData->getMax();
}

double Input_SingleStreamAlg::getEsp()
{
	return m_dEsp;
}

int Input_SingleStreamAlg::getDataLength()
{
	return m_pRawData->size();
}

DataItem Input_SingleStreamAlg::getAt(int index)
{
	return m_pRawData->getAt(index);
}

#endif
