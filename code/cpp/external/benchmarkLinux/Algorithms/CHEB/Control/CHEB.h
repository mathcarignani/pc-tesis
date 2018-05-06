#ifndef __CHEB_H
#define __CHEB_H

#pragma once

#include "../../Algo.h"
#include "../Data/CHEBInput.h"
#include "../Data/CHEBOutput.h"

class CHEB : public Algo
{
private:
	CHEBInput *m_input;
	CHEBOutput *m_output;
	double	m_dSeg_Length;
	int		m_nChevSize;

public:
	CHEB(void);
	CHEB(CHEBInput *pInputData, double seg_Length, int nLength);
	~CHEB(void);

	double* getInputData();
	void setInputData(CHEBInput *pInputData);

	virtual Output* getOutput();

	virtual void compress();
};

#endif
