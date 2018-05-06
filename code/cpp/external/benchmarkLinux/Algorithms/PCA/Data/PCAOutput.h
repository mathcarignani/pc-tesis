#ifndef __PCAOUTPUT_H
#define __PCAOUTPUT_H

#pragma once

#include "../../../DataStructures/DynArray/DynArray.cpp"
#include "../../../DataManagementLayer/Data/Output.h"
#include "../../../DataManagementLayer/Data/DataStream.h"
#include "PCAEntry.h"
#include "PCAInput.h"

class PCAOutput: public Output
{
private:
	PCAInput* m_pInputData;
	DynArray<PCAEntry>* m_pCompressedData;
	CDataStream*        m_pApproxData;

	// location for result files
	char* m_sFolderPath_compressedData;
	char* m_sFolderPath_approxData;

public:
	PCAOutput(PCAInput* inputData);
	~PCAOutput(void);

	// Calculate approximation data from model parameters
	void decompress();

	// Add new compressed item(PCAEntry object) for compressed output data
	void addNew_compressedItem(double value, bool isRawData);

	virtual double  getCompressionRatio();
	virtual double  getUpdateFrequency();
	virtual double  getRMSE();

	// Get file path to save for approximate data and output
	virtual void    getParameter(char** parameters,int paraCount);

	// Write compressed data and approximate data
	virtual void    write_output_to_File();

	// Write compressed data
	void write_output_to_File(char* filename);

	// Write approx data
	void write_ApproxData_to_File(char* filename);
};

#endif
