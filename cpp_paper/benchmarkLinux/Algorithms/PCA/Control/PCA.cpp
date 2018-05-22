#ifndef __PCAALG_CPP
#define __PCAALG_CPP

#include "PCA.h"
#include "assert.h"

PCA::PCA(PCAInput * input)
{
	m_pInput = input;
	m_pOutput = new PCAOutput(m_pInput);
}

PCA::~PCA(void)
{
	delete m_pInput;
	delete m_pOutput;
}

Output* PCA::getOutput()
{
	return m_pOutput;
}

// Purpose	: Compress a given window data and add result to output
// Parameter: (In) wndData: Raw window data												
//				   length  : Length of window data											
void PCA:: add2Output(double* wndData, int length)
{
	double min = wndData[0];
	double max = wndData[0];
	for (int i = 0; i < length; i++)
	{
		if (wndData[i] < min)
			min = wndData[i];
		if (wndData[i] > max)
			max = wndData[i];
	}

	if ((max-min) < 2*m_pInput->getEsp())
	{
		m_pOutput->addNew_compressedItem((max - min) / 2 + min, false);
	}
	else
	{
		for(int i = 0; i < length; i++)
		{
			m_pOutput->addNew_compressedItem(wndData[i], true);
		}
	}
}

// compress raw data
void PCA::compress()
{
	int wndSize = m_pInput->getWndSize();
	assert (wndSize > 0);

	int dataLength = m_pInput -> getDataLength();
	double* wndData = new double[wndSize];

	int executionPos = 0;
	while(executionPos < dataLength)
	{
		m_pInput->getWndData(executionPos, wndData);

		//Compress for each window size
		if (executionPos + wndSize <= dataLength)
		{
			add2Output(wndData,wndSize);
			executionPos += wndSize;
		}
		else // Compress for last window size
		{
			add2Output(wndData,dataLength - executionPos);
			executionPos = dataLength;
		}
	}

	delete[] wndData;
}

#endif