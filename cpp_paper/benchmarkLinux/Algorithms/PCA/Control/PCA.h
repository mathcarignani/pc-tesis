#ifndef __PCAALG_H
#define __PCAALG_H

#pragma once

#include "../../Algo.h"
#include "../Data/PCAOutput.h"

class PCA : public Algo
{
private:
	PCAInput * m_pInput;
	PCAOutput * m_pOutput;

public:
	PCA(PCAInput * mInput);
	~PCA(void);

	virtual Output* getOutput();
	void add2Output(double* wndData, int length);// Compress a given window data and add result to output

	virtual void compress();// compress raw data
};

#endif
