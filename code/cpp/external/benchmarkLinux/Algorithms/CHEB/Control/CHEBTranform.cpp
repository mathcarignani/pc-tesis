#ifndef _CHEBTranform_CPP
#define _CHEBTranform_CPP

#include "CHEBTranform.h"
#include "../../../stdafx.h"

double  f (double x, void *p)
{
 
	int a;
	double * q;
	a = (int) (floor(x + 0.5));
	q = (double*) p;
	return q[a];
}

CHEBTransform::CHEBTransform(void)
{
}

// Parameter:	dInput  : Raw data array														   
//				nSize	: the size of raw data array(it is also the order of Chebyshev polinomial 
//				a		: the lower bound of Chebyshev algorithm								   
//				b		: the upper bound of Chebyshev algorithm								   
//				dEsp	: the threshold of Chebyshev algorithm									   
CHEBTransform::CHEBTransform(double *dInput, int nSize, double a, double b, double dEsp)
{
	m_nNumOfCoeff = nSize;
	m_dLowerBound = a;
	m_dUpperBound = b;
	m_dEsp = dEsp;
	
	// Empty the content
	for(; m_arrRawData.size() > 0;)
	{
		m_arrRawData.remove();
	}

	for(int i = 0; i < m_nNumOfCoeff; i++)
	{
		m_arrRawData.add(dInput[i]);
	}

	// Create Chebyshev series
	calulateCHEVCoeff();
}

CHEBTransform::~CHEBTransform(void)
{
	gsl_cheb_free(m_cs);
}

// Calculate the Chebyshev coeficient							
void CHEBTransform::calulateCHEVCoeff()
{
    int i = 0; 
    double * input = (double*) malloc(m_nNumOfCoeff * sizeof(double));
    m_cs = gsl_cheb_alloc (m_nNumOfCoeff - 1);
    gsl_function F;

	for (i=0; i < m_nNumOfCoeff; i++)
    {   
	    // Set the input param for function
		input[i] = (double) (m_arrRawData.getAt(i));
    }
 
    F.function = f;
    F.params = input;
 
	// Initialize the Chebyshev series
	gsl_cheb_init (m_cs, &F, m_dLowerBound, m_dUpperBound);
  
	// Get Chebyshev result to array
	// Empty content of Chebyshev Coefficient array
	for(; m_arrChevCoefficients.size() > 0;)
	{
		m_arrChevCoefficients.remove();
	}

	// Make the list of Chebyshev Coefficient
	for(i = 0; i < m_nNumOfCoeff; i++)
	{
		m_arrChevCoefficients.add(m_cs->c[i]);
	}

	// Free memory
    free(input);
}

// Purpose	: Get the error of Chebyshev algorithm with raw data											
// Parameter: cs : a pointer which hold the Chebyshev series struct							
double CHEBTransform::calError(gsl_cheb_series *cs)
{
	double x = 0;
	double dTemp = 0, dMax = 0;
	double dRawValue;
	double dChebValue;

	for(int i = 0; i < m_nNumOfCoeff; i++)
	{
		x			=	(double) i;
		dRawValue	=	m_arrRawData.getAt(i);
		dChebValue	=	gsl_cheb_eval (cs, x);
		dTemp		=   abs(dRawValue - dChebValue);
		if(dTemp > dMax)
		{
			dMax = dTemp;
		}
	}
	return dMax;
}

// Purpose	: Sort Chebyshev coefficients descently															
// Parameter: (In): dInputCoeffArray : The unsorted Chebyshev coefficients array				
//					OutputCoeffArray : The output descending sorted coefficients with these other	
void CHEBTransform::DescCoeffSort(double *dInputCoeffArray, DynArray<CHEBCoeffEntry> &OutputCoeffArray/*the output coefficients with these others*/)
{
	int nCount;
	int nCount1;
	CHEBCoeffEntry TempEntry;

	for(nCount = 0; nCount < m_nNumOfCoeff; nCount++)
	{
		CHEBCoeffEntry Entry(dInputCoeffArray[nCount], nCount);
		OutputCoeffArray.add(Entry);
	}

	// Buble sorting
	for(nCount = 0; nCount < m_nNumOfCoeff - 1; nCount++)
	{
		for(nCount1 = m_nNumOfCoeff -1 ; nCount1 > nCount; nCount1--)
		{
			if(abs(OutputCoeffArray.getAt(nCount1).dCoeff) > abs(OutputCoeffArray.getAt(nCount1 - 1).dCoeff))
			{
				TempEntry = OutputCoeffArray.getAt(nCount1);
				OutputCoeffArray.replace(nCount1, OutputCoeffArray.getAt(nCount1 - 1));
				OutputCoeffArray.replace(nCount1 - 1, TempEntry);
			}
		}
	}

}

// Purpose	: Compress data after applying Chebyshev algorithm with fixed espsilon								
// Parameter: chevCoefficients : The Chebyshev coeficients array								
// Return	: bool - true : Compress successfully													
//			:	   - false: otherwise																
bool CHEBTransform::compressData(DynArray<double>* chevCoefficients)
{
	bool bIsCommpressed = false;
	int i = 0, j = 0, k = 0;	 
	double *dInputArray = (double*) malloc(m_nNumOfCoeff * sizeof(double));
	for(i = 0; i < m_nNumOfCoeff; i++)
	{
		dInputArray[i] = m_cs->c[i];
		if(chevCoefficients->size() > 0)
		{
			chevCoefficients->remove();
		}
	}

	// Initialize an output Chebyshev series
	gsl_cheb_series* outputChevSeries;
	outputChevSeries = gsl_cheb_alloc(m_nNumOfCoeff);
	outputChevSeries->a = m_cs->a;
	outputChevSeries->b = m_cs->b;
	outputChevSeries->order = m_cs->order;
	outputChevSeries->order_sp = m_cs->order_sp;
	memcpy(outputChevSeries->c, m_cs->c, m_nNumOfCoeff * sizeof(double));
	memcpy(outputChevSeries->f, m_cs->f, m_nNumOfCoeff * sizeof(double));

	//	Sort Coefficients descending
	DynArray<CHEBCoeffEntry> DesSortCoeffArr;
	DescCoeffSort(dInputArray, DesSortCoeffArr);

	// Calculate the Commpressed Coefficients
	for(i = 1; i < m_nNumOfCoeff; i++)
	{
		for(j = 0; j < m_nNumOfCoeff; j++)
		{
			outputChevSeries->c[j] = 0;
		}

		for(j = 0; j < i; j++)
		{
			 k = DesSortCoeffArr.getAt(j).nOrder;
			 outputChevSeries->c[k] = DesSortCoeffArr.getAt(j).dCoeff;
		}

		// Calculate an Error
		if(calError(outputChevSeries) < m_dEsp)
		{
			// If compressing successfully, set the output Coefficients
			for(j = 0; j < m_nNumOfCoeff; j++)
			{
				chevCoefficients->add(outputChevSeries->c[j]);
			}
			bIsCommpressed = true;
			break;
		}

	}

	// Assign values for Coefficient array in case compressing unsuccsefully
	if(chevCoefficients->size() <= 0)
	{
		for(i = 0; i < m_nNumOfCoeff; i++)
		{
			chevCoefficients->add(m_arrRawData.getAt(i));
		}
	}

	// Free the memory
	free(dInputArray);
	gsl_cheb_free(outputChevSeries);
	
	return bIsCommpressed;
}

#endif