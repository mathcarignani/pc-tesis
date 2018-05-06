#ifndef _CHEBTranform_H
#define _CHEBTranform_H

#pragma once

#include "../../../DataStructures/DynArray/DynArray.cpp"
#include "../Transform/gsl_chebyshev.h"

#define		NUM_OF_INPUT_POINT		16

struct CHEBCoeffEntry
{
	double dCoeff;
	int nOrder;
	CHEBCoeffEntry(double a, int b)
	{
		dCoeff = a;
		nOrder = b;
	};
	CHEBCoeffEntry(){};
};


class CHEBTransform
{
private:
	DynArray<double> m_arrRawData;
	DynArray<double> m_arrChevCoefficients;
	DynArray<double> m_arrCompressedChevCoefficients;

	gsl_cheb_series *m_cs;

	int m_nNumOfCoeff;
	double m_dMax;
	double m_dEsp;
	double m_dLowerBound;
	double m_dUpperBound;

	// Calculate the Chebyshev coeficient							
	void calulateCHEVCoeff();

	// Get the error of Chebyshev algorithm with raw data											
	double calError(gsl_cheb_series *cs);

	// Sort Chebyshev coefficients descently															
	void DescCoeffSort(double *dInputCoeffArray, DynArray<CHEBCoeffEntry> &OutputCoeffArray/*the output coefficients with these others*/);

public:
	CHEBTransform(void);
	CHEBTransform(double* dInput, int nSize, double a, double b, double dEsp); 
	~CHEBTransform(void);

	// Compress data after applying Chebyshev algorithm with fixed espsilon
	bool compressData(DynArray<double>* chevCoefficients /*output parameter*/);
};

#endif