#ifndef __EXPMULTI_H
#define __EXPMULTI_H

#include "../stdafx.h"
#include <stdio.h>
#include <iostream>
//#include <conio.h>
#include <time.h>

// Run multi-stream algorithm for all frequencies and thresholds
static void GAMPS_Alg(int nNumOfEsp, double *dEspArray, int nNumOfFrequency, int *nFreqArray, DataLoader *dataLoader)
{
	// Read input data
	char* directory = new char[200];
	int fileCount = 0;
	Config::getString((char*)"gamps",(char*)"folderPath_input",directory);
	char** inputPaths = ReadDir(directory, fileCount);
	if(fileCount <= 0)
	{
		delete[] directory;
		delete[] inputPaths;
		return;
	}

	// Read config
	char* data_category = new char[100];
	Config::getString((char*)"run",(char*)"data_category",data_category);
	int outlier = Config::getInt((char*)"run",(char*)"outlier");

	// Metrics array for staticstic information
	double *dRMSEStaticstic	= (double*) malloc(sizeof(double) * nNumOfEsp * sizeof(int) * nNumOfFrequency);
	double *dTimeStaticstic	= (double*) malloc(sizeof(double) * nNumOfEsp * sizeof(int) * nNumOfFrequency);
	double *dRatioStaticstic= (double*) malloc(sizeof(double) * nNumOfEsp * sizeof(int) * nNumOfFrequency);

	// Run for each frequency and threshold
	double eps = 0;
	int gampsUpdateFrequenty = 1;
	double dRunningTime = 0;
	int inputDataSize = 0;
	for(int FreqCount = 0; FreqCount < nNumOfFrequency; FreqCount++)
	{
		// Get update frequency
		gampsUpdateFrequenty = nFreqArray[FreqCount];

		for(int EspCount = 0; EspCount < nNumOfEsp; EspCount++)
		{
			inputDataSize = 0;

			// Multi-stream input data
			char** fileNames = new char*[fileCount];
			CMultiDataStream* multiStream = new CMultiDataStream(fileCount);

			for(int i = 0; i < fileCount; i++)
			{
				char* fileName = GetFileName(inputPaths[i]);
				CDataStream* signal = dataLoader-> read_from_File(inputPaths[i],gampsUpdateFrequenty);
				inputDataSize = inputDataSize + signal->size();
				multiStream->addSingleStream(signal);
				fileNames[i] = fileName;
			}

			// Add outlier
			if (outlier !=0)
				multiStream->addOutlier(outlier);

			GAMPSInput* gampsInput = new GAMPSInput(multiStream);

			// Get Epsilon value
			eps = dEspArray[EspCount];
			char EspValue[10];
			::memset(EspValue, 0, sizeof(char) * 10);
			sprintf(EspValue,"%2.5f",eps);
			char FrequencyValue[10];
			::memset(FrequencyValue, 0, sizeof(char) * 10);
			::itoa(gampsUpdateFrequenty, FrequencyValue, 10);
            //itoa(gampsUpdateFrequenty, FrequencyValue, 10);

			// Setup output folders
			char* compressFolder = new char[MAX_PATH];
			::memset(compressFolder, 0, sizeof(char) * MAX_PATH);
			char* approxFolder = new char[MAX_PATH];
			::memset(approxFolder, 0, sizeof(char) * MAX_PATH);
			char* basePath = new char[MAX_PATH];
			::memset(basePath, 0, sizeof(char) * MAX_PATH);
			char* basePrefix = new char[200];
			::memset(basePrefix, 0, sizeof(char) * 200);
			char* ratioPath = new char[MAX_PATH];
			::memset(ratioPath, 0, sizeof(char) * MAX_PATH);
			char* ratioPrefix = new char[200];
			::memset(ratioPrefix, 0, sizeof(char) * 200);
			char* approxFile = new char[MAX_PATH];
			::memset(approxFile, 0, sizeof(char) * MAX_PATH);
			char* approxPrefix = new char[200];
			::memset(approxPrefix, 0, sizeof(char) * 200);

			Config::getString((char*)"gamps",(char*)"folderPath_output",compressFolder);
			Config::getString((char*)"gamps",(char*)"prefix_baseSignal",basePrefix);
			Config::getString((char*)"gamps",(char*)"prefix_ratioSignal",ratioPrefix);
			Config::getString((char*)"gamps",(char*)"folderPath_output",approxFolder);
			Config::getString((char*)"gamps",(char*)"prefix_Approx",approxPrefix);

			strcat(compressFolder, "/compressedData/");
			strcat(approxFolder, "/approxData/");
			CreateDir(compressFolder);
			CreateDir(approxFolder);

			// Create eps_frequency directory
			char* epsFrequencyDir = new char[200];
			::memset(epsFrequencyDir, 0, sizeof(char) * 200);

			strcat(epsFrequencyDir,EspValue);
			strcat(epsFrequencyDir,"_");
			strcat(epsFrequencyDir,FrequencyValue);

			// Compress data folders
			strcat(basePath, compressFolder);
			strcat(basePath, epsFrequencyDir);
			CreateDir(basePath);
			strcat(basePath, "/");
			strcat(basePath,basePrefix);

			strcat(ratioPath, compressFolder);
			strcat(ratioPath, epsFrequencyDir);
			strcat(ratioPath, "/");
			strcat(ratioPath, ratioPrefix);

			// Approx data folders
			strcat(approxFile, approxFolder);
			strcat(approxFile, epsFrequencyDir);
			CreateDir(approxFile);
			strcat(approxFile, "/");
			strcat(approxFile, approxPrefix);

			// Setup output folders and parameters for each run
			char** parameter = new char*[3];
			parameter[0] = basePath;
			parameter[1] = ratioPath;
			parameter[2] = approxFile;

			// Run algorithm & measure performance
			GAMPS* gamps = new GAMPS(eps,gampsInput);

			__int64  nStart= 0, nEnd = 0, nFreq = 0;
            //int64_t  nStart= 0, nEnd = 0, nFreq = 0;
			QueryPerformanceCounter((LARGE_INTEGER *)&nStart);

			gamps->compute();

			QueryPerformanceCounter((LARGE_INTEGER *)&nEnd);
			QueryPerformanceFrequency((LARGE_INTEGER *)&nFreq);

			double duration = (nEnd - nStart) * 1.0 / nFreq;
			dRunningTime =  dRunningTime + duration/inputDataSize;

			// Write output to file
			gamps->getOutput()->getParameter(parameter,3);
			gamps->getOutput()->setInputFileNames(fileNames);
			double compressRatio = gamps->getOutput()->getCompressionRatio();
			double rmse = gamps->getOutput()->getRMSE();
			gamps->getOutput()->write_output_to_File();

			// Free memory
			delete[] basePath;
			delete[] ratioPath;
			delete[] approxFile;
			delete[] parameter;
			delete[] basePrefix;
			delete[] ratioPrefix;
			delete[] approxPrefix;
			delete[] compressFolder;
			delete[] approxFolder;
			delete[] epsFrequencyDir;
			for(int i = 0; i< fileCount; i++)
			{
				delete[] fileNames[i];
			}
			delete[] fileNames;
			delete gamps;
			delete gampsInput;


			// Output metrics
			dRatioStaticstic[FreqCount * nNumOfEsp + EspCount] = compressRatio;
			dRMSEStaticstic[FreqCount * nNumOfEsp + EspCount] = rmse;
			dTimeStaticstic[FreqCount * nNumOfEsp + EspCount] = dRunningTime;

			// Re-initialize for next run
			compressRatio = 0;
			rmse = 0;
			dRunningTime = 0;
		}
	}

	// Free memory
	delete[] directory;
	for(int i = 0; i< fileCount; i++)
	{
		delete[] inputPaths[i];
	}
	delete[] inputPaths;

	// Write statistic information into file
	char filePath[MAX_PATH];
	::memset(filePath, 0, sizeof(char) * MAX_PATH);

	Config::getString((char*)"GAMPS", (char*)"folderPath_output", filePath);
	strcat(filePath,"/statistic/");
	CreateDir(filePath);
	strcat(filePath,"Ratio.txt");
	writeStatistics(filePath, data_category, (char*)"GAMPS", (char*)"CmpRatio", outlier, dRatioStaticstic, nNumOfEsp, dEspArray , nNumOfFrequency, nFreqArray);

	Config::getString((char*)"GAMPS", (char*)"folderPath_output", filePath);
	strcat(filePath,"/statistic/");
	strcat(filePath,"RMSE.txt");
	writeStatistics(filePath, data_category, (char*)"GAMPS",(char*)"RMSERatio", outlier, dRMSEStaticstic, nNumOfEsp, dEspArray , nNumOfFrequency, nFreqArray);

	Config::getString((char*)"GAMPS", (char*)"folderPath_output", filePath);
	strcat(filePath,"/statistic/");
	strcat(filePath,"Time.txt");
	writeStatistics(filePath, data_category, (char*)"GAMPS",(char*)"Time", outlier, dTimeStaticstic, nNumOfEsp, dEspArray , nNumOfFrequency, nFreqArray);

	// Free staticstic memory
	free(dRatioStaticstic);
	free(dRMSEStaticstic);
	free(dTimeStaticstic);

	// Free memory
	delete[] data_category;
}

#endif
