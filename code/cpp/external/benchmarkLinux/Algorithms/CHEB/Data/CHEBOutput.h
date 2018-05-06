#ifndef __CHEBOUTPUT_H
#define __CHEBOUTPUT_H

#pragma once

#include "ApproxPolynomial.h"
#include "../../../DataStructures/DynArray/DynArray.cpp"
#include "../../../DataManagementLayer/Data/Output.h"

class CHEBOutput : public Output
{
private:
	DynArray<CApproxPolynomial*> m_compressedData;
	DynArray<double>* m_OutputArray;
	DynArray<double>* m_InputArray;

	// location for result files
	char* m_sFolderPath_compressedData;
	char* m_sFolderPath_approxData;

public:
	CHEBOutput(void);
	~CHEBOutput(void);

	//Add a new approximate polynomial data to [m_compressData] variable
	void addNewOutput(CApproxPolynomial* p);

	//Set the input data which is get from raw data stream to [m_InputArray] variable
	void setInputArray(double* dInputData, int size);

	//Get the number of Non-zero Chevbyshev coefficients
	int getNumOfNonZeroCoeffs();

	//Decompress approximate data and recover the real data
	DynArray<double>* decompress();

	virtual double getCompressionRatio();
	virtual double getUpdateFrequency();
	virtual double getRMSE();

	//Get file path to save for approximate data and output
	virtual void getParameter(char** parameters,int paraCount);

	// Write compressed data and approximate data
	virtual void write_output_to_File();

	// Write compressed data
	void write_output_to_File(char* filename);

	// Write approx data
	void write_ApproxData_to_File(char* filename);
};

#endif
