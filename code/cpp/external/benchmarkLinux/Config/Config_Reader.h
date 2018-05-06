#ifndef __CONFIG_READER_H
#define __CONFIG_READER_H

#include "../stdafx.h"
//#include "windows.h"
#include "string.h"
#include "time.h"
#include "Config.h"

// Read the epsilon array in the configuration file
static double* GetEspArray(int &nNumOfEsp/*output para: number of Epsilon */)// , double *dEspArray /*output para: Epsilon array*/)
{
	nNumOfEsp = Config::getInt((char*)"input", (char*)"numOfEsp");
	double *dEpsArray = (double*) (malloc(sizeof(double) * nNumOfEsp));

	// Process to get all esp
	char* EpsRawArray = new char[300];
	Config::getString((char*)"INPUT",(char*)"esp",EpsRawArray);
	char* EpsValueString =  strtok (EpsRawArray,";");

	for(int i = 0; i < nNumOfEsp; i++)
	{
		char temp[10];
		double dEpsValue = 0;
		::memset(temp, 0, sizeof(char) * 10);
		strcpy(temp,EpsValueString);

		// Get Epsilon value
		dEpsValue = ::atof(temp);
		dEpsArray[i] = dEpsValue;

		EpsValueString = strtok (NULL,";");
	}

	delete[] EpsRawArray;
	return dEpsArray;
}

// Read the frequency array in the configuration file
static int* GetUpdateFrequency(int &nNumOfFreq)
{
	nNumOfFreq = Config::getInt((char*)"input", (char*)"numOfUpdateFrequency");
	int *dFreqArray = (int*) (malloc(sizeof(int) * nNumOfFreq));
    //printf("%d\n",nNumOfFreq);
	// Process to get all frequencies
	char* FreqRawArray = new char[300];
	Config::getString((char*)"INPUT",(char*)"update_frequency",FreqRawArray);
	char* FreqValueString =  strtok (FreqRawArray,";");
	for(int i = 0; i < nNumOfFreq; i++)
	{
		char temp[10];
		int dFreqValue = 0;
		::memset(temp, 0, sizeof(char) * 10);
		strcpy(temp,FreqValueString);
		// Get frequency value
		dFreqValue = ::atoi(temp);
		dFreqArray[i] = dFreqValue;

		FreqValueString = strtok (NULL,";");
	}

	delete[] FreqRawArray;
	return dFreqArray;
}
#endif
