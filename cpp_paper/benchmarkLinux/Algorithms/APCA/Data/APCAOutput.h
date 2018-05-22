#ifndef __APCAOUTPUT_H
#define __APCAOUTPUT_H

#include "../../../stdafx.h"
#include "../../../DataStructures/DynArray/DynArray.cpp"
#include "APCAEntry.h"
#include "../../../DataManagementLayer/Data/Output.h"
#include "../../../DataManagementLayer/Data/DataStream.h"
#include "APCAInput.h"

class APCAOutput: public Output
{
private:
	APCAInput* m_pInputData;
	DynArray<APCAEntry>* m_pCompressData;
	CDataStream* m_pApproxData;

	// location for result files
	char* m_sFolderPath_CompressedData;
	char* m_sFolderPath_ApproxData;

public:
	APCAOutput(APCAInput* pInputData);
	~APCAOutput(void);

	DynArray<APCAEntry>* getCompressData();
	void  setCompressData(DynArray<APCAEntry>* compressData);

	// Calculate approximation data from model parameters
	void  decompressData();

	virtual double  getCompressionRatio();
	virtual double  getUpdateFrequency();
	virtual double  getRMSE();

	// Get file path to save for approximate data and output
	virtual void    getParameter(char** parameters,int paraCount);

	// Write compressed data and approximate data
	virtual void    write_output_to_File();

	// Write compressed data
	void    write_output_to_File(char* filename);

	// Write approximate data
	void    write_ApproxData_to_File(char* filename);
};

#endif
