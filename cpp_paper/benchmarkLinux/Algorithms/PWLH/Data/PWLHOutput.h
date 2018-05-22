#ifndef __PWLHOUTPUT_H
#define __PWLHOUTPUT_H

#pragma once
#include "../../../DataManagementLayer/Data/Output.h"
#include "../../../DataManagementLayer/Data/DataStream.h"
#include "../../../DataStructures/Line/Line.h"
#include "../../../DataStructures/DynArray/DynArray.cpp"
#include "PWLHInput.h"

class PWLHOutput : public Output
{
private:
	PWLHInput* m_pInputData;
	DynArray<Point>* m_pCompressData;
	CDataStream* m_pApproxData;

	// location for result files
	char* outputFilePath;
	char* appropriateFilePath;

public:
	PWLHOutput(PWLHInput* originalData);
	~PWLHOutput(void);

	DynArray<Point>* getCompressData();

	// Calculate approximation data from model parameters
	void decompressData();

	virtual double getCompressionRatio();
	virtual double getUpdateFrequency();
	virtual double getRMSE();

	// Get file path to save for approximate data and output
	virtual void getParameter(char** parameters,int paraCount);

	// Write compressed data and approximate data
	virtual void write_output_to_File();

	// Write compressed data
	void write_output_to_File(char* filename);

	// Write approximate data
	void write_ApproxData_to_File(char* filename);
};

#endif
