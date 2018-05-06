#ifndef __PWLHOUTPUT_CPP
#define __PWLHOUTPUT_CPP

#include "../../../stdafx.h"
#include "PWLHOutput.h"
#include "../../../DataStructures/Line/Line.h"

// Add ----> A
//#include <crtdbg.h>
// Add <---- A

//Add ----> A
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif
// Add <---- A

PWLHOutput::PWLHOutput(PWLHInput *originalData)
{
	m_pInputData = originalData;
	m_pCompressData = new DynArray<Point>();
}

PWLHOutput::~PWLHOutput(void)
{
	delete m_pCompressData;
	delete m_pApproxData;
}

DynArray<Point>* PWLHOutput::getCompressData()
{
	return m_pCompressData;
}

// Calculate approximation data from model parameters
void PWLHOutput::decompressData()
{
	m_pApproxData = new CDataStream();
	Point p1, p2;
	Line* l = NULL;
	DataItem inputEntry;
	int size = m_pCompressData->size();
	int position = 0;
	int timeStamp = 0;
	int lastTimeStamp = m_pCompressData->getAt(m_pCompressData->size() - 1).x;

	for(int i = 0; i < lastTimeStamp; i++)
	{
		if(i >= timeStamp)
		{
			p1 = m_pCompressData->getAt(position);
			position++;
			if (position < size)
			{
				p2 = m_pCompressData->getAt(position);
				timeStamp = p2.x;
				if (l != NULL)	delete l;
				l = new Line(&p1, &p2);
				position++;
			}
			else
			{
				inputEntry.timestamp = p1.x;
				inputEntry.value = p1.y;
				m_pApproxData->add(inputEntry);
				break;
			}
		}

		inputEntry.timestamp = i + 1;
		inputEntry.value = l->getValue(i + 1);
		m_pApproxData->add(inputEntry);
	}

	delete l;
}

double PWLHOutput::getCompressionRatio()
{
	// Calculate original data size
	double returnValue = 0;
	int signalLength = m_pInputData->getDataLength();
	int inputElementSize= DOUBLE_SIZE;
	int inputMemory = signalLength * inputElementSize;

	// Calculate compress data size
	int compressLength = m_pCompressData->size();
	int outputElementSize = DOUBLE_SIZE + INT_SIZE;
	int outputMemory = compressLength * outputElementSize;

	returnValue =(double)outputMemory / (double)inputMemory;
	return returnValue;
}

double PWLHOutput::getUpdateFrequency()
{
	double returnValue = 0;
	int signalLength = m_pInputData->getDataLength();

	// Get number of segments
	int compressLength = m_pCompressData->size();
	returnValue =(double)compressLength / (double)(2 * signalLength);
	return returnValue;
}

double PWLHOutput::getRMSE()
{
	// Decompress data
	decompressData();

	// Calculate RMSE
	double returnValue = 0;
	int dataSize = m_pApproxData->size();
	for(int i = 0; i < dataSize; i++)
	{
		double inputValue = m_pInputData->getAt(i).value;
		double decompressValue = m_pApproxData->getAt(i).value;
		double temp = decompressValue - inputValue;
		temp = pow(temp,2);
		returnValue = returnValue + temp;
	}
	returnValue = sqrt(returnValue / dataSize);

	//Normalize RMSE with respect to data range
	return returnValue / (m_pInputData->getMaxValue() - m_pInputData->getMinValue());
}

// Purpose	: Get file path to save for approximate data and output
// Parameter: (In) : parameters: An array pointer which helds the file path
//			         paraCount : Number of output file paths
void PWLHOutput::getParameter(char **parameters, int paraCount)
{
	if(paraCount == 2)
	{
		outputFilePath = parameters[0];
		appropriateFilePath = parameters[1];
	}
	else
	{
		printf("-----------------------Invalid parameters----------------------------\n");
		printf("SlideFilters must have 2 para: outputFilePath,appropriatePath \n");
		printf("---------------------------------------------------------------------\n");
	}
}

// Write compressed data and approximate data
void PWLHOutput::write_output_to_File()
{
	write_output_to_File(outputFilePath);
	write_ApproxData_to_File(appropriateFilePath);
}

// Write compressed data
void PWLHOutput::write_output_to_File(char *filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		for (int i = 0; i < m_pCompressData->size(); i++)
		{
			char *buffer = new char[50];
			::memset(buffer,0,sizeof(char)*50);
			char *date = new char[20];
			::memset(date,0,sizeof(char)*20);
			char *num = new char[20];
			::memset(num,0,sizeof(char)*20);
			Point point = m_pCompressData->getAt(i);
			sprintf(date,"%.5f", point.x);
			sprintf(num,"%.5f", point.y);
			strcpy(buffer, date);
			strcat(buffer,",");
			strcat(buffer, num);

			fputs(buffer, file);
			if (i != m_pCompressData->size() -1)
			{
				fputs("\n", file);
			}

			delete buffer;
			delete date;
			delete num;
		}
		fclose (file);
	}
}

// Write approximate data
void PWLHOutput::write_ApproxData_to_File(char *filename)
{
	FILE *file = fopen(filename, "w");
	if (file == NULL) perror ("Error opening file");
	else
	{
		for (int i = 0; i < m_pApproxData->size(); i++)
		{
			char *buffer = new char[50];
			::memset(buffer,0,sizeof(char)*50);
			char *date = new char[20];
			::memset(date,0,sizeof(char)*20);
			char *num = new char[20];
			::memset(num,0,sizeof(char)*20);
			DataItem entry = m_pApproxData->getAt(i);
			itoa(entry.timestamp, date, 10);
			sprintf(num,"%.5f", entry.value);
			strcat(buffer, num);

			fputs(buffer, file);
			if (i != m_pApproxData->size() -1)
			{
				fputs("\n", file);
			}

			delete num;
			delete buffer;
			delete date;
		}
		fclose (file);
	}
}

#endif
