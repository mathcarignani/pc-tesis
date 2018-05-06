#ifndef __APCA_CPP
#define __APCA_CPP

#include "../../../stdafx.h"
#include "APCA.h"

APCA::APCA(APCAInput* pInput)
{
	m_pInput = pInput;
	m_pOutput = new APCAOutput(m_pInput);
}

APCA::~APCA()
{
	delete m_pOutput;
	delete m_pInput;
}

Output* APCA::getOutput()
{
	return m_pOutput;
}

// Compute model parameters
void APCA::compress()
{
	double curMax = 0;
	double curMin = 0;
	double doubleEsp = 2 * m_pInput->getEsp();
	int  inputLength = m_pInput->getDataLength();

	if(inputLength <= 0) return;

	DataItem item  = m_pInput->getAt(0);
	curMax  = item.value;
	curMin  = item.value;
	DynArray<APCAEntry>* compressData = new DynArray<APCAEntry>();

	for(int i = 0; i < inputLength; i++)
	{
		double tempMax  = curMax;
		double tempMin  = curMin;
		DataItem item = m_pInput->getAt(i);
		double newValue = item.value;
		if(curMax < newValue) tempMax = newValue;
		if(curMin > newValue) tempMin = newValue;

		//new value makes the height of current bucket greater than 2 epsilon
		if((tempMax - tempMin) > doubleEsp)
		{
			//close and add current bucket to compressData
			APCAEntry compress;
			compress.value = (curMax + curMin)/2;
			compress.endingTimestamp = item.timestamp - 1;
			compressData->add(compress);

			//create new bucket
			curMax = newValue;
			curMin = newValue;
		}
		else
		{
			curMax = tempMax;
			curMin = tempMin;
		}
	}

	//add the last bucket
	APCAEntry entry;
	entry.value = (curMax + curMin) / 2;
	entry.endingTimestamp = inputLength;
	compressData->add(entry);

	//Set compressed data
	m_pOutput->setCompressData(compressData);
};

#endif
