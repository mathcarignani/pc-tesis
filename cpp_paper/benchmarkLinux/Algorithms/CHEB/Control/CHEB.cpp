#ifndef __CHEB_CPP
#define __CHEB_CPP

#include "CHEB.h"
#include "CHEBTranform.h"

CHEB::CHEB(void)
{
	m_output = new CHEBOutput();
}

// Parameter:	pInputData : Raw data which are held by CHEBInput object					  
//				seg_Length : the window data length											  
//				nLength	   : the lower bound of Chevbyshev algorithm						  
CHEB::CHEB(CHEBInput *pInputData, double seg_Length, int nLength)
{
	m_input			=	pInputData;
	m_dSeg_Length	=	seg_Length;
	m_nChevSize		=	nLength;
	m_output		=	new CHEBOutput();
}

CHEB::~CHEB()
{
	if (m_input != NULL)	delete m_input;
	if (m_output != NULL)	delete m_output;
}

double* CHEB::getInputData()
{
	return m_input->getWndData(0, m_input->getDataLength());
}

void CHEB::setInputData(CHEBInput *pInputData)
{
	m_input = pInputData;
}

Output* CHEB::getOutput()
{
	return m_output;
}

// Applying Chevbyshev algorithm														  
void CHEB::compress()
{
	bool bIsCompressed = false;
	int nFrom = 0, nTo = m_input->getDataLength();
	double *dInputSeg = NULL;
	CApproxPolynomial *approxPoly;

	// Loop for each input data segment
	for(nFrom = 0; nFrom < nTo - m_dSeg_Length; nFrom += m_dSeg_Length)
	{
		// Get raw window data
		dInputSeg = m_input->getWndData(nFrom, m_dSeg_Length);

		// Initialize Chevbyshev transformation object
		CHEBTransform chevTrans(dInputSeg, m_dSeg_Length, 0, m_dSeg_Length - 1, m_input->getEsp());
		DynArray<double> outDynArr ;

		// Trying compress data
		bIsCompressed = chevTrans.compressData(&outDynArr);

		// If successful, add the compress data to Approximate polynomial
		if(bIsCompressed)
		{
			approxPoly = new CApproxPolynomial(m_dSeg_Length, &outDynArr, 0, m_dSeg_Length - 1, false);
		}
		// Otherwise, keep the raw data for output
		else
		{
			approxPoly = new CApproxPolynomial(m_dSeg_Length, &outDynArr, 0, m_dSeg_Length - 1, true);
		}
		m_output->addNewOutput(approxPoly);
		if(dInputSeg != NULL)
		{
			delete []dInputSeg;
		}
	}

	// Get the last output segment
	dInputSeg = m_input->getWndData(nFrom, nTo - nFrom);
	CHEBTransform chevTrans(dInputSeg, nTo - nFrom, 0, nTo - nFrom - 1, m_input->getEsp());
	DynArray<double> outDynArr ;

	bIsCompressed = chevTrans.compressData(&outDynArr);
	if(bIsCompressed)
	{
		approxPoly = new CApproxPolynomial(nTo - nFrom, &outDynArr, 0, m_dSeg_Length - 1, false);
	}
	else
	{
		approxPoly = new CApproxPolynomial(nTo - nFrom, &outDynArr, 0, m_dSeg_Length - 1, true);
	}
	m_output->addNewOutput(approxPoly);

	m_output->setInputArray(getInputData(), m_input->getDataLength());

	if(dInputSeg != NULL)
	{
		delete []dInputSeg;
	}
}

#endif