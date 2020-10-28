#ifndef __GAMPS_CPP
#define __GAMPS_CPP

#include "../../../stdafx.h"
#include "GAMPS.h"

GAMPS::GAMPS(GAMPSInput* data)
{
	m_pGampsInput = data;
	m_nNumOfStream = data->getNumOfStream();
	m_pGampsCompute = new GAMPS_Computation(m_pGampsInput);
}

GAMPS::~GAMPS()
{
	delete m_pGampsCompute;
}

// Execute GAMPS algorithm
void GAMPS::compute(int m_dEps)
{
	m_pGampsCompute->statGroup(m_dEps);
	m_pGampsOutput = m_pGampsCompute->getGampsOutput();
}

GAMPSOutput* GAMPS::getOutput()
{
	return m_pGampsOutput;
}

#endif
