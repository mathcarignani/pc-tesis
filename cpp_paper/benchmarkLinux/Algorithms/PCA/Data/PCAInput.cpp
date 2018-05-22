#ifndef __PCAINPUT_CPP
#define __PCAINPUT_CPP

#include "PCAInput.h"

// Purpose	: Constructor														  
// Parameter: (In): rawData  : The raw data stream						          
//					wndSize  : the size of window data							  
//					esp	  : the threshold of PCA algorithm					  
PCAInput::PCAInput(CDataStream* rawData, int wndSize, double esp):Input_SingleStreamAlg(rawData, esp)
{
	m_nWndSize = wndSize;
}

int PCAInput::getWndSize()
{
	return m_nWndSize;
}

// Purpose	: Get 'm_nWndSize' values which start from 'from' position																		
// Parameter: (In) : from       : The position in draw data stream which is used to get window data	
//			  (Out): arrWndData : The window data get from raw data stream 							
void PCAInput::getWndData(int from, double* arrWndData)
{
	for (int i = 0; (i < m_nWndSize) && (i + from < m_pRawData->size()); i++)
	{
		arrWndData[i] = m_pRawData->getAt(from + i).value;
	}
}

#endif