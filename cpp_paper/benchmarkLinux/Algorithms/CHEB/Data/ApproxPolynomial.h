#ifndef __APPROXPOLYNOMIAL_H
#define __APPROXPOLYNOMIAL_H

#pragma once
#include "../Transform/gsl_chebyshev.h"
#include "../../../DataStructures/DynArray/DynArray.cpp"

class CApproxPolynomial
{
private:
	// maximum number of CHEV coefficient
	int m_nNumOfCoeff;
	// list of coeffs from 0 to (m_numOfCoeff -1)
	double* m_dCoeffs;
	double m_dLowerBound;
	double m_dUpperBound;

	// the flag which decide data is Approximate polynomial or Raw data
	bool m_bIsRawData;

public:
	CApproxPolynomial(void);
	CApproxPolynomial(int nNumOfCoeff, double* dNumOfCoeff, 
						double dLowerBound,double dUpperBound, 
						bool bIsRawData = false);
	CApproxPolynomial(int nNumOfCoeff, DynArray<double>* dNumOfCoeff, 
						double dLowerBound,double dUpperBound, 
						bool bIsRawData = false);
	~CApproxPolynomial(void);

	double * getApproxValues();
	double * getCoeffs();
	int getNumOfCoeff();
	int getNumOfNonZeroCoeffs();
	bool isRawData()
	{
		return m_bIsRawData;
	}
};

#endif