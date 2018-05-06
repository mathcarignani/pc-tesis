#ifndef __CHEBOUTPUT_CPP
#define __CHEBOUTPUT_CPP

#include "../../../stdafx.h"
#include "CHEBOutput.h"

CHEBOutput::CHEBOutput(void)
{
	m_OutputArray = NULL;
	m_InputArray = NULL;
}

CHEBOutput::~CHEBOutput(void)
{
	// Free output array
	if(m_OutputArray != NULL)
	{
		if(m_OutputArray->size() > 0)
		{
			delete m_OutputArray;
		}
	}

	// Free Input array
	if(m_InputArray != NULL)
	{
		if(m_InputArray->size() > 0)
		{
			delete m_InputArray;
		}
	}

	// Free each approximate polynomial data in m_commpressData array
	if(m_compressedData.size() > 0)
	{
		for(int i = 0; i < m_compressedData.size(); i++)
		{
			delete (m_compressedData.getAt(i));
		}
	}
}

// Purpose	: Add a new approximate polynomial data to [m_compressData] variable
// Parameter: p : An approximate polynomial which is used to add
void CHEBOutput::addNewOutput(CApproxPolynomial *p)
{
	m_compressedData.add(p);
}

// Purpose	: Set the input data which is get from raw data stream to [m_InputArray] variable
// Parameter:	dInputData: a double array which hold the input values
//			    size	  : a size of input array
void CHEBOutput::setInputArray(double* dInputData, int size)
{
	m_InputArray = new DynArray<double>();
	for(int i = 0; i < size; i++)
	{
		m_InputArray->add(dInputData[i]);
	}
	free(dInputData);
}

// Purpose	: Get the number of Non-zero Chevbyshev coefficients
// Return	: (int) - A number of Non-zero Chevbyshev coefficients
int CHEBOutput::getNumOfNonZeroCoeffs()
{
	int nNumOfNonZeroCoeffs = 0;

	// Loop all the approximate polynomials
	for(int i = 0; i < m_compressedData.size(); i++)
	{
		// Get the number none-zero coefficients of each approximate polynomial
		nNumOfNonZeroCoeffs += m_compressedData.getAt(i)->getNumOfNonZeroCoeffs();
	}
	return nNumOfNonZeroCoeffs;
}

// Purpose	: Decompress approximate data and recover the real data
// Return	: DynArray<double>* : A pointer of an output array which held the recover data
DynArray<double>* CHEBOutput::decompress()
{
	DynArray<double>* outputArray = new DynArray<double>();
	double *temp;
	int i = 0, j = 0;

	// Loop by the numbers of window length
	for(i = 0; i < m_compressedData.size(); i++)
	{
		// Get approximate value from Chevbyshev approximate polinomial
		temp = m_compressedData.getAt(i)->getApproxValues();
		// Loop by the numbers of data in each window
		for(j = 0; j < m_compressedData.getAt(i)->getNumOfCoeff(); j++)
		{
			//  Add an approximate values to output data
			outputArray->add(temp[j]);
		}
		free(temp);
	}

	// Keep output array by output member varialbe
	m_OutputArray = outputArray;
	outputArray = NULL;

	return m_OutputArray;
}

double CHEBOutput::getCompressionRatio()
{
	int nLength					=	m_OutputArray->size();
	int	nNumOfNonZeroCoeff		=	getNumOfNonZeroCoeffs();
	double	dTotalOriginalSize	=	nLength * DOUBLE_SIZE;
	double	dTotalControlWords	=	0;
	double	totalCompressedSize	=	0;
	double	dCompressionRatio	=	0;

	// Get Compressed data size
	dTotalControlWords			= ((int) ((nLength / 8) + 0.5));

	totalCompressedSize =	(nNumOfNonZeroCoeff * DOUBLE_SIZE) + dTotalControlWords;

	// Calculate the ratio
	dCompressionRatio	=	totalCompressedSize / dTotalOriginalSize;

	return dCompressionRatio;
}

double CHEBOutput::getUpdateFrequency()
{
	return (double)getNumOfNonZeroCoeffs()/m_InputArray->size();
}

double CHEBOutput::getRMSE()
{
	// Decompress data
	decompress();

	// Calculate RMSE
	double dRMSE = 0;
	double dEsp = 0;
	double min, max;
	if (m_InputArray->size() > 0)
	{
		min = 0;
		max = 0;
	}
	for(int i = 0; i < m_OutputArray->size(); i++)
	{
		dEsp	=	::pow(m_InputArray->getAt(i) - m_OutputArray->getAt(i), 2);
		dRMSE	+=	dEsp;

		if (min > m_InputArray->getAt(i))
			min =  m_InputArray->getAt(i);

		if (max < m_InputArray->getAt(i))
			max = m_InputArray->getAt(i);

	}
	dRMSE		=	::sqrt(dRMSE / m_OutputArray->size()) ;

	//Normalize RMSE with respect to data range
	return dRMSE/(max-min);
}

// Purpose	: Get file path to save for approximate data and output
// Parameter: (In) : parameters: An array pointer which helds the file path
//			         paraCount : Number of output file paths
void CHEBOutput::getParameter(char** parameters,int paraCount)
{
	if(paraCount == 2)
	{
		m_sFolderPath_compressedData = parameters[0];
		m_sFolderPath_approxData = parameters[1];
	}
	else
	{
		printf("-----------------------Invalid parameters----------------------------\n");
		printf("CHEB algorithm requires 2 para: folderPath_compressedData ,folderPath_approxData \n");
		printf("---------------------------------------------------------------------\n");
	}

}

// Write compressed data and approximate data
void CHEBOutput::write_output_to_File()
{
	write_output_to_File(this->m_sFolderPath_compressedData);
	write_ApproxData_to_File(this->m_sFolderPath_approxData);
}

// Write compressed data
void CHEBOutput::write_output_to_File(char *filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		for (int i = 0; i < this->m_compressedData.size(); i++)
		{
			CApproxPolynomial* entry = this->m_compressedData.getAt(i);
			char* isRawData = (entry->isRawData())? (char*)"1":(char*)"0";

			double* coeffs = entry->getCoeffs();
			int numOfNonZeroCoeffs = entry->getNumOfNonZeroCoeffs();
			for (int j = 0; j < numOfNonZeroCoeffs; j++)
			{
				char buffer[20];
				char num[10];
				memset(buffer, 0, sizeof(char) * 20);
				memset(num, 0, sizeof(char) * 10);

				strcat(buffer, isRawData);
				sprintf(num,"%.5f", coeffs[j]);
				strcat(buffer,",");
				strcat(buffer, num);

				fputs(buffer, file);

				if (j != numOfNonZeroCoeffs - 1)
				{
					fputs("\n", file);
				}


			}

			free(coeffs);

			if (i != this->m_compressedData.size() - 1)
			{
				fputs("\n", file);
			}
		}
		fclose (file);
	}
}

// Write approximate data
void CHEBOutput::write_ApproxData_to_File(char* filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		for (int i=0; i < m_OutputArray->size(); i++)
		{
			char *buffer = new char[30];
			char *date = new char[30];
			char *num = new char[30];
			::memset(buffer, 0, sizeof(char) * 30);
			::memset(date, 0, sizeof(char) * 30);
			::memset(num, 0, sizeof(char) * 30);

			double value = m_OutputArray->getAt(i);
			itoa(i + 1, date, 10);
			sprintf(num,"%.5f", value);
			strcat(buffer, num);

			fputs(buffer, file);
			if (i != m_OutputArray->size() -1)
			{
				fputs("\n", file);
			}

			delete []buffer;
			delete []date;
			delete []num;
		}
		fclose (file);
	}
}

#endif
