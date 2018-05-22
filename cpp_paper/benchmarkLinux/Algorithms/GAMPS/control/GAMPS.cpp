#ifndef __GAMPS_CPP
#define __GAMPS_CPP

#include "../../../stdafx.h"
#include "GAMPS.h"

GAMPS::GAMPS(double eps,GAMPSInput* data)
{
	m_dEps = eps;
	m_pGampsInput = data;
	m_nNumOfStream = data->getNumOfStream();
	m_pGampsCompute = new GAMPS_Computation(m_pGampsInput,m_dEps);
}

GAMPS::~GAMPS()
{
	delete m_pGampsCompute;
}

// Execute GAMPS algorithm
void GAMPS::compute()
{
	m_pGampsCompute->statGroup();
	m_pGampsOutput = m_pGampsCompute->getGampsOutput();
}

GAMPSOutput* GAMPS::getOutput()
{
	return m_pGampsOutput;
}

#endif
