#ifndef __INPUT_SINGLESTREAM_H
#define __INPUT_SINGLESTREAM_H

#pragma once

#include "DataStream.h"

//Inputs for single stream algorithm
class Input_SingleStreamAlg
{
protected:
	CDataStream* m_pRawData; // Raw data of stream
	double m_dEsp; // Error tolerance

public:
	Input_SingleStreamAlg(CDataStream* rawData, double esp);

	double  getMinValue();
	double  getMaxValue();
	double  getEsp();
	int     getDataLength();

	DataItem getAt(int index);
};

#endif
