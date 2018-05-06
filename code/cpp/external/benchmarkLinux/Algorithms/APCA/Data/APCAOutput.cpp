#ifndef __APCAOUTPUT_CPP
#define __APCAOUTPUT_CPP

#include "APCAOutput.h"

APCAOutput::APCAOutput(APCAInput* input)
{
	m_pInputData = input;
	m_pApproxData = new CDataStream();
}

APCAOutput::~APCAOutput()
{
	delete m_pApproxData;
	delete m_pCompressData;
}

DynArray<APCAEntry>* APCAOutput::getCompressData()
{
	return m_pCompressData;
}

void APCAOutput::setCompressData(DynArray<APCAEntry>* compressData)
{
	m_pCompressData = compressData;
}

// Calculate approximation data from model parameters
void APCAOutput::decompressData()
{
	if (m_pCompressData->size() ==0)
		return;

	APCAEntry lastBucket = m_pCompressData->getAt(m_pCompressData->size() - 1);
	int lastTimeStamp = lastBucket.endingTimestamp;
	int indexOfCurBucket = 0;

	APCAEntry curBucket  =  m_pCompressData->getAt(0);
	for(int i = 1; i <= lastTimeStamp; i++)
	{
		if(i > curBucket.endingTimestamp)
		{
			indexOfCurBucket++;
			curBucket  =  m_pCompressData->getAt(indexOfCurBucket);
		}
		DataItem approxItem;
		approxItem.timestamp = i;
		approxItem.value = curBucket.value;
		m_pApproxData->add(approxItem);
	}
}

double APCAOutput::getCompressionRatio()
{
	// Calculate original data size
	int inputLength = m_pInputData->getDataLength();
	int inputElementMemory= DOUBLE_SIZE;
	int inputMemory = inputLength * inputElementMemory;

	// Calculate compress data size
	int compressLength = m_pCompressData->size();
	int compressElementMemory = DOUBLE_SIZE + INT_SIZE;
	int compressMemory = compressLength * compressElementMemory;

	double ratio =(double)compressMemory / (double)inputMemory;
	return ratio;
}

double APCAOutput::getUpdateFrequency()
{
	int inputLength = m_pInputData->getDataLength();

	// Get number of segments
	int compressLength = m_pCompressData->size();

	double ratio =(double)compressLength/(double)inputLength;
	return ratio;
}

double APCAOutput::getRMSE()
{
	// Decompress data
	decompressData();

	// Calculate RMSE
	double rmse = 0;
	int dataSize = m_pApproxData->size();

	for(int i = 0; i < dataSize; i++)
	{
		double inputValue = m_pInputData->getAt(i).value;
		double approxValue = m_pApproxData->getAt(i).value;
		double error = approxValue - inputValue;
		error = pow(error,2);
		rmse = rmse + error;
	}

	rmse = sqrt(rmse / dataSize);

	//Normalize RMSE with respect to data range
	double maxValue = m_pInputData->getMaxValue();
	double minValue = m_pInputData->getMinValue();
	double range    = maxValue - minValue;

	return rmse/range;
}

// Purpose	: Get file path to save for approximate data and output
// Parameter: (In) : parameters: An array pointer which helds the file path
//			         paraCount : Number of output file paths
void APCAOutput::getParameter(char** parameters,int paraCount)
{
	if(paraCount == 2)
	{
		m_sFolderPath_CompressedData = parameters[0];
		m_sFolderPath_ApproxData = parameters[1];
	}
	else
	{
		printf("-----------------------Invalid parameters----------------------------\n");
		printf("APCAOutput must have 2 para: m_sFolderPath_CompressedData, appropriatePath \n");
		printf("---------------------------------------------------------------------\n");
	}
}

// Write compressed data and approximate data
void APCAOutput::write_output_to_File()
{
	write_output_to_File(m_sFolderPath_CompressedData);
	write_ApproxData_to_File(m_sFolderPath_ApproxData);
}

// Write compressed data
void APCAOutput::write_output_to_File(char* filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		char* buffer = new char[30];
		::memset(buffer,0,sizeof(char)*30);
		char* date = new char[10];
		::memset(date,0,sizeof(char)*10);
		char* num = new char[20];
		::memset(num,0,sizeof(char)*20);

		for (int i = 0; i < m_pCompressData->size(); i++)
		{
			strcpy(buffer,"");
			APCAEntry entry = m_pCompressData->getAt(i);
			itoa(entry.endingTimestamp, date, 10);
			sprintf(num,"%.5f", entry.value);
			strcat(buffer, date);
			strcat(buffer,",");
			strcat(buffer, num);

			fputs(buffer, file);
			if (i != m_pCompressData->size() -1)
			{
				fputs("\n", file);
			}
		}
		delete[] buffer;
		delete[] date;
		delete[] num;
		fclose (file);
	}
}

// Write approximate data
void APCAOutput::write_ApproxData_to_File(char* filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		char* buffer = new char[30];
		::memset(buffer,0,sizeof(char)*30);
		char* date = new char[10];
		::memset(date,0,sizeof(char)*10);
		char* num = new char[20];
		::memset(num,0,sizeof(char)*20);

		for (int i = 0; i < m_pApproxData->size(); i++)
		{
			strcpy(buffer,"");
			DataItem item = m_pApproxData->getAt(i);
			itoa(item.timestamp, date, 10);
			sprintf(num,"%.5f", item.value);
			strcat(buffer, num);

			fputs(buffer, file);
			if (i != m_pApproxData->size() -1)
			{
				fputs("\n", file);
			}
		}
		delete[] buffer;
		delete[] date;
		delete[] num;
		fclose (file);
	}
}

#endif
