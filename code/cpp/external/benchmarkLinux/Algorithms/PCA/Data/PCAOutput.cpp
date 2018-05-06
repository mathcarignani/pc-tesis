#ifndef __PCAOUTPUT_CPP
#define __PCAOUTPUT_CPP

#include "../../../stdafx.h"
#include "PCAOutput.h"

PCAOutput::PCAOutput(PCAInput* inputData)
{
	m_pInputData = inputData;
	m_pCompressedData = new DynArray<PCAEntry>();
	m_pApproxData     = new CDataStream();
	m_sFolderPath_compressedData  = NULL;
	m_sFolderPath_approxData      = NULL;
}

PCAOutput::~PCAOutput(void)
{
	delete m_pCompressedData;
	delete m_pApproxData;
}

// Calculate approximation data from model parameters
void PCAOutput::decompress()
{
	double length_compressedData = m_pCompressedData->size();
	int curPos = 0;

	for (int i = 0; i < length_compressedData; i++)
	{
		PCAEntry compressedItem =  m_pCompressedData->getAt(i);
		if (compressedItem.m_isRawData == false)
		{
			for(int j = 0; j < m_pInputData->getWndSize(); j++)
			{
				DataItem approxItem;
				approxItem.timestamp = curPos;
				approxItem.value = compressedItem.m_dValue;
				m_pApproxData->add(approxItem);
				curPos++;
				if (curPos >= m_pInputData->getDataLength())
					break;
			}
		}
		else
		{
			DataItem* inputEntry = new DataItem();
			inputEntry->timestamp = curPos;
			inputEntry->value = compressedItem.m_dValue;
			m_pApproxData->add(*inputEntry);

			delete inputEntry;
			curPos++;
		}
	}
}

// Purpose	: Add new compressed item(PCAEntry object) for compressed output data
// Parameter: (In) : value     : Value of compressd data
//			         isRawData : A flag which indicated that compressed data is raw data or not
void PCAOutput::addNew_compressedItem(double value, bool isRawData)
{
	PCAEntry newItem;
	newItem.m_dValue = value;
	newItem.m_isRawData = isRawData;
	m_pCompressedData->add(newItem);
}

double PCAOutput::getCompressionRatio()
{
	// Calculate original data size
	int inputLength = m_pInputData->getDataLength();
	int inputElementMemory= DOUBLE_SIZE;
	int inputMemory = inputLength * inputElementMemory;

	// Calculate compress data size
	int compressLength = m_pCompressedData->size();
	int compressElementMemory = DOUBLE_SIZE + 1;
	int compressMemory = compressLength * compressElementMemory;

	double ratio =(double)compressMemory/(double)inputMemory;
	return ratio;
}

double PCAOutput::getUpdateFrequency()
{
	int inputLength = m_pInputData->getDataLength();

	// Get number of segments
	int compressLength = m_pCompressedData->size();

	double ratio =(double)compressLength/(double)inputLength;
	return ratio;
}

double PCAOutput::getRMSE()
{
	// Decompress data
	decompress();

	// Calculate RMSE
	double rmse = 0;
	for (int i=0; i< m_pInputData->getDataLength(); i++)
	{
		double inputValue = m_pInputData->getAt(i).value;
		double approxValue = m_pApproxData->getAt(i).value;
		rmse += pow(inputValue - approxValue,2);
	}
	rmse /= m_pInputData->getDataLength();

	//Normalize RMSE with respect to data range
	return sqrt(rmse)/(m_pInputData->getMaxValue() - m_pInputData->getMinValue());
}

// Purpose	: Get file path to save for approximate data and output
// Parameter: (In) : parameters: An array pointer which helds the file path
//			         paraCount : Number of output file paths
void PCAOutput::getParameter(char** parameters,int paraCount)
{
	if(paraCount == 2)
	{
		m_sFolderPath_compressedData = parameters[0];
		m_sFolderPath_approxData = parameters[1];
	}
	else
	{
		printf("-----------------------Invalid parameters----------------------------\n");
		printf("PCA algorithm requires 2 para: folderPath_compressedData ,folderPath_approxData \n");
		printf("---------------------------------------------------------------------\n");
	}
}

// Write compressed data and approximate data
void PCAOutput::write_output_to_File()
{
	write_output_to_File(m_sFolderPath_compressedData);
	write_ApproxData_to_File(m_sFolderPath_approxData);
}

// Write compressed data
void PCAOutput::write_output_to_File(char* filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		for (int i = 0; i < m_pCompressedData->size(); i++)
		{
			char buffer[20];
			char num[10];
			memset(buffer, 0, sizeof(char) * 20);
			memset(num, 0, sizeof(char) * 10);
			PCAEntry entry = m_pCompressedData->getAt(i);
			const char* isRawData = (entry.m_isRawData)? "1":"0";
			sprintf(num,"%.5f", entry.m_dValue);
			strcat(buffer, isRawData);
			strcat(buffer,",");
			strcat(buffer, num);

			fputs(buffer, file);
			if (i != m_pInputData->getDataLength() -1)
			{
				fputs("\n", file);
			}
		}
		fclose (file);
	}
}

// Write approximate data
void PCAOutput::write_ApproxData_to_File(char* filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		for (int i = 0; i < m_pInputData->getDataLength(); i++)
		{
			char buffer[20];
			char date[10];
			char num[20];
			memset(buffer,0, sizeof(char) * 20);
			memset(date,0, sizeof(char) * 10);
			memset(num,0, sizeof(char) * 10);

			DataItem entry = m_pApproxData->getAt(i);
			itoa(entry.timestamp + 1, date, 10);
			sprintf(num,"%.5f", entry.value);
			strcat(buffer, num);

			fputs(buffer, file);
			if (i != m_pInputData->getDataLength() -1)
			{
				fputs("\n", file);
			}
		}
		fclose (file);
	}
}

#endif
