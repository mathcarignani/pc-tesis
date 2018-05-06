#ifndef __APPROXPOLYNOMIAL_CPP
#define __APPROXPOLYNOMIAL_CPP

#include "../../../stdafx.h"
#include "ApproxPolynomial.h"
#include <math.h>

CApproxPolynomial::CApproxPolynomial(void)
{
}

// Parameter:	nNumOfCoeff  : the order of Chevbyshev polynomial						
//				dNumOfCoeff	 : the Chevbyshev coefficients array 						
//				dLowerBound	 : the lower bound of Chevbyshev algorithm					
//				dUpperBound	 : the upper bound of Chevbyshev algorithm					
//				bIsRawData	 : the flag indicate this polynomial data is raw data or not
CApproxPolynomial::CApproxPolynomial(int nNumOfCoeff, double *dNumOfCoeff, 
									 double dLowerBound, double dUpperBound, bool bIsRawData)
{
	m_nNumOfCoeff	=	nNumOfCoeff;
	m_dLowerBound	=	dLowerBound;
	m_dUpperBound	=	dUpperBound;
	m_bIsRawData	=	bIsRawData;
	m_dCoeffs = (double*) (malloc(m_nNumOfCoeff * sizeof(double)));
	::memcpy(m_dCoeffs, dNumOfCoeff, m_nNumOfCoeff * sizeof(double));	
}

// Parameter:	nNumOfCoeff  : the order of Chevbyshev polynomial						
//				dNumOfCoeff	 : the Chevbyshev coefficients array(use DynArray object	
//				dLowerBound	 : the lower bound of Chevbyshev algorithm					
//				dUpperBound	 : the upper bound of Chevbyshev algorithm					
//				bIsRawData	 : the flag indicate this polynomial data is raw data or not
CApproxPolynomial::CApproxPolynomial(int nNumOfCoeff, DynArray<double> *dNumOfCoeff, 
									 double dLowerBound, double dUpperBound, bool bIsRawData)
{
	m_nNumOfCoeff	=	nNumOfCoeff;
	m_dLowerBound	=	dLowerBound;
	m_dUpperBound	=	dUpperBound;
	m_bIsRawData	=	bIsRawData;
	m_dCoeffs = (double*) (malloc(m_nNumOfCoeff * sizeof(double)));
	for(int i = 0; i < m_nNumOfCoeff; i++)
	{
		m_dCoeffs[i] = dNumOfCoeff->getAt(i);
	}
}

CApproxPolynomial::~CApproxPolynomial(void)
{
	free(m_dCoeffs);
}

// Purpose	: Get the Chevbyshev approximate values from approximate polynomial					
// Return	: double* : A pointer of an output array which held the approximate data			
double* CApproxPolynomial::getApproxValues()
{
	double* dApproxValue = (double*) (malloc(m_nNumOfCoeff * sizeof(double)));
	
	// If Chevbyshev algorithm can not compress and return raw value, the approximate values are raw data
	if(m_bIsRawData)
	{
		for(int i = 0; i < m_nNumOfCoeff; i++)
		{
			dApproxValue[i] = m_dCoeffs[i];
		}
	}
	// If Chevbyshve algorithm can compress data, the approximate values are calculated by Chevbyshev formula
	else
	{
		for(int i = 0; i < m_nNumOfCoeff; i++)
		{
			dApproxValue[i] = gsl_cheb_eval1(m_dCoeffs, m_nNumOfCoeff, m_dLowerBound, m_dUpperBound, i);
		}
	}

	return dApproxValue;
}

// Purpose	: Get the Chevbyshev coefficient values from the approximate polynomial
// Return	: double* : A pointer of an output array which held the coefficient data
double* CApproxPolynomial::getCoeffs()
{
	if (m_bIsRawData)
	{
		double* dCoeffs = (double*) (malloc(m_nNumOfCoeff * sizeof(double)));

		for (int i = 0; i < m_nNumOfCoeff; i++)
		{
			dCoeffs[i] = m_dCoeffs[i];
		}

		return dCoeffs;
	}

	int nNumOfNonZeroCoeffs = getNumOfNonZeroCoeffs();
	double* dCoeffs = (double*) (malloc(nNumOfNonZeroCoeffs * sizeof(double)));
	
	int j = 0;
	for (int i = 0; i < m_nNumOfCoeff; i++)
	{
		if (abs(m_dCoeffs[i]) > 0.0001)// Not equal to zero
		{
			dCoeffs[j] = m_dCoeffs[i];
			j++;
		}
	}

	return dCoeffs;
}

// Purpose	: Get the number of Chevbyshev coefficients(the Chevbyshev polynomial order			
// Return	: int : the number of Chevbyshev coefficients										
int CApproxPolynomial::getNumOfCoeff()
{
	return m_nNumOfCoeff;
}

// Purpose	: Get the number of Non-zero Chevbyshev coefficients in approximate polynomial		
// Return	: int : the number of Non-zero Chevbyshev coefficients										
int	CApproxPolynomial::getNumOfNonZeroCoeffs()
{
	// If Chevbyshev algorithm can not compress, return the Chevbyshev order
	if(m_bIsRawData)
	{
		return m_nNumOfCoeff;
	}

	int nNumOfNonZeroCoeffs = 0;
	for(int i = 0; i < m_nNumOfCoeff; i++)
	{
		// if(m_dCoeffs[i] != 0)
		if (abs(m_dCoeffs[i]) > 0.0001)// Not equal to zero
		{
			nNumOfNonZeroCoeffs++;
		}
	}
	return nNumOfNonZeroCoeffs;
}

#endif