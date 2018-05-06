#ifndef __EXPSINGLE_H
#define __EXPSINGLE_H

#include "../stdafx.h"
#include <stdio.h>
#include <iostream>
//#include <conio.h>
#include <time.h>

// Create folders for outputs
void setupFolder(char* algo, char* compressFolder, char* compressPrefix, char* approxFolder, char* approxPrefix)
{
	::memset(compressFolder,0,sizeof(char)*MAX_PATH);
	::memset(compressPrefix,0,sizeof(char)*MAX_PATH);
	::memset(approxFolder,0,sizeof(char)*MAX_PATH);
	::memset(approxPrefix,0,sizeof(char)*MAX_PATH);

	Config::getString(algo,(char*)"folderPath_output",compressFolder);
	Config::getString(algo,(char*)"folderPath_output",approxFolder);
	Config::getString(algo,(char*)"prefix_compressedData",compressPrefix);
	Config::getString(algo,(char*)"prefix_approxData",approxPrefix);

	strcat(compressFolder, "/compressedData/");
	strcat(approxFolder, "/approxData/");
	CreateDir(compressFolder);
	CreateDir(approxFolder);
}

// Write statistics information into file
static void statistics(char* data_category, char* algo, char* metric, double outlier, double *dStatistics, int nNumOfEps, double* dEpsArray, int nNumOfFreq, int *nFreqArray)
{
	char filePath[MAX_PATH];
	::memset(filePath, 0, sizeof(char) * MAX_PATH);

	Config::getString(algo, (char*)"folderPath_output", filePath);
	strcat(filePath,"/statistic/");
	CreateDir(filePath);
	strcat(filePath, metric);
	strcat(filePath,".txt");

	writeStatistics(filePath, data_category, algo, metric, outlier, dStatistics, nNumOfEps, dEpsArray , nNumOfFreq, nFreqArray);
}

// Setup output folders and parameters for each run
static void setupParameters(char* algo, double eps, int bucketUpdateFrequenty, char* fileName, char* &tempCompressPath, char* &tempApproxPath)
{
	char EspValue[10];
	char FrequencyValue[10];
	::memset(EspValue, 0, sizeof(char) * 10);
	::memset(FrequencyValue, 0, sizeof(char) * 10);
	sprintf(EspValue,"%2.5f",eps);
	::itoa(bucketUpdateFrequenty, FrequencyValue, 10);

	char* compressFolder = new char[MAX_PATH];
	char* compressPrefix = new char[MAX_PATH];
	char* approxFolder = new char[MAX_PATH];
	char* approxPrefix = new char[MAX_PATH];

	setupFolder(algo, compressFolder, compressPrefix, approxFolder, approxPrefix);

	char* epsFrequencyDir = new char[200];
	::memset(epsFrequencyDir, 0, sizeof(char) * 200);
	strcat(epsFrequencyDir,EspValue);
	strcat(epsFrequencyDir,"_");
	strcat(epsFrequencyDir,FrequencyValue);

	/********* Compress data *************/
	strcat(tempCompressPath,compressFolder);
	strcat(tempCompressPath,epsFrequencyDir);
	CreateDir(tempCompressPath);
	strcat(tempCompressPath,"/");
	strcat(tempCompressPath,compressPrefix);
	strcat(tempCompressPath,fileName);

	/********* Approximate data ***********/
	strcat(tempApproxPath,approxFolder);
	strcat(tempApproxPath,epsFrequencyDir);
	CreateDir(tempApproxPath);
	strcat(tempApproxPath,"/");
	strcat(tempApproxPath,approxPrefix);
	strcat(tempApproxPath,fileName);

	delete[] compressFolder;
	delete[] approxFolder;
	delete[] approxPrefix;
	delete[] compressPrefix;

	delete[] epsFrequencyDir;
}

// Run single-stream algorithm for a given frequency and threshold
static void runAlg(char* algo, int outlier, double eps, int bucketUpdateFrequenty, DataLoader *dataLoader, double &dCompressRatio, double &dSegmentRatio, double &dRMSE, double &dRunningTime)
{
	// Setup parameters
	dCompressRatio = 0;
	dSegmentRatio = 0;
	dRMSE = 0;
	dRunningTime = 0;

	char EspValue[10];
	char FrequencyValue[10];
	::memset(EspValue, 0, sizeof(char) * 10);
	::memset(FrequencyValue, 0, sizeof(char) * 10);
	sprintf(EspValue,"%2.5f",eps);
	::itoa(bucketUpdateFrequenty, FrequencyValue, 10);

	// Get config
	char* directory = new char[MAX_PATH];
	::memset(directory,0,sizeof(char)*MAX_PATH);
	Config::getString(algo,(char*)"folderPath_input",directory);

	// Setup input data
	int fileCount = 0;
	char** inputPaths = ReadDir(directory,fileCount);
    //printf("%d\n",fileCount);

	int numOfValidFile =0;
	for(int i = 0; i < fileCount; i++)
	{
		// Load input data
		CDataStream* dataStream = dataLoader-> read_from_File(inputPaths[i],bucketUpdateFrequenty);
		if (dataStream->size() == 0)
		{
			delete dataStream;
			continue;
		}
		numOfValidFile++;

		char* tempCompressPath = new char[200];
		char* tempApproxPath = new char[200];
		char* fileName;
		::memset(tempCompressPath,0,sizeof(char)*200);
		::memset(tempApproxPath,0,sizeof(char)*200);
		fileName = GetFileName(inputPaths[i]);

		// Setup output folders and parameters for each run
		char** parameter = new char*[2];
		setupParameters(algo, eps, bucketUpdateFrequenty, fileName, tempCompressPath, tempApproxPath);
		parameter[0] =  tempCompressPath;
		parameter[1] =  tempApproxPath;

		// Statistics information of input data
		dataStream->statistic();

		if (outlier !=0)
		{
			dataStream->addOutlier(outlier);
		}

		// Run algorithm & measure performance
		Algo* algoObj;

		if(!strcmp(strupr(algo), "APCA"))
		{
			APCAInput* bucketInput = new APCAInput(dataStream,eps);
			algoObj = new APCA(bucketInput);
		}
		else if(!strcmp(strupr(algo), "GAMPS"))
		{

		}
		else if(!strcmp(strupr(algo), "SF"))
		{
			SlideFiltersInput* slideFiltersInput = new SlideFiltersInput(dataStream, eps);
			algoObj = new SlideFilters(slideFiltersInput);
		}
		else if(!strcmp(strupr(algo), "CHEB"))
		{
			CHEBInput* inputData = new CHEBInput(dataStream, eps);
			double seg_length = Config::getDouble((char*)"CHEB", (char*)"seg_length");
			algoObj = new CHEB(inputData, seg_length , dataStream->size());
		}
		else if(!strcmp(strupr(algo), "PCA"))
		{
			int nWndSize = Config::getInt((char*)"PCA",(char*)"window_size");
			PCAInput* pPCAInput = new PCAInput(dataStream, nWndSize, eps);
			algoObj = new PCA(pPCAInput);
		}
		else if(!strcmp(strupr(algo), "PWLH"))
		{
			PWLHInput* histogramInput = new PWLHInput(dataStream, eps);
			algoObj = new PWLH(histogramInput);
		}

		//__int64  nStart= 0, nEnd = 0, nFreq = 0;
        int64_t  nStart= 0, nEnd = 0, nFreq = 0;
		QueryPerformanceCounter((LARGE_INTEGER *)&nStart);

		algoObj->compress();

		QueryPerformanceCounter((LARGE_INTEGER *)&nEnd);
		QueryPerformanceFrequency((LARGE_INTEGER *)&nFreq);
		double duration = (nEnd - nStart) * 1.0 / nFreq;
		dRunningTime =  dRunningTime + duration/dataStream->size();

		// Write output to file
		algoObj->getOutput()->getParameter(parameter,2);
		dRMSE += algoObj->getOutput()->getRMSE();
		dCompressRatio += algoObj->getOutput()->getCompressionRatio();
		dSegmentRatio += algoObj->getOutput()->getUpdateFrequency();

		algoObj->getOutput()->write_output_to_File();

		// Free memory
		delete dataStream;
		delete algoObj;
		delete[] parameter;
		delete[] tempCompressPath;
		delete[] tempApproxPath;
		delete[] fileName;
	}

	// Output metrics
	dCompressRatio = dCompressRatio / numOfValidFile;
	dSegmentRatio = dSegmentRatio / numOfValidFile;
	dRMSE = dRMSE / numOfValidFile;
	dRunningTime = dRunningTime / numOfValidFile;

	// Free memory
	delete[] directory;
	for(int i = 0; i< fileCount; i++)
	{
		delete[] inputPaths[i];
	}
	delete[] inputPaths;
}

// Run single-stream algorithm for all frequencies and thresholds
static void SingleStream_Alg(char* algo, int nNumOfEsp, double *dEspArray, int nNumOfFrequency, int *nFreqArray, DataLoader *dataLoader)
{
	// Read config
	char* data_category = new char[100];
	Config::getString((char*)"run",(char*)"data_category",data_category);
	int outlier = Config::getInt((char*)"run",(char*)"outlier");

	// Metrics array for staticstic information
	double *dRMSEStaticstic	= (double*) malloc(sizeof(double) * nNumOfEsp * sizeof(int) * nNumOfFrequency);
	double *dTimeStaticstic	= (double*) malloc(sizeof(double) * nNumOfEsp * sizeof(int) * nNumOfFrequency);
	double *dCompressionRatioStaticstic= (double*) malloc(sizeof(double) * nNumOfEsp * sizeof(int) * nNumOfFrequency);
	double *dSegmentRatioStaticstic= (double*) malloc(sizeof(double) * nNumOfEsp * sizeof(int) * nNumOfFrequency);

	// Run for each frequency and threshold
	double eps = 0;
	int bucketUpdateFrequenty = 1;
	for(int FreqCount = 0; FreqCount < nNumOfFrequency; FreqCount++)
	{
		// Get update frequency
		bucketUpdateFrequenty = nFreqArray[FreqCount];
        //printf("%d\n",bucketUpdateFrequenty);

		for(int EspCount = 0; EspCount < nNumOfEsp; EspCount++)
		{
			// Get epsilon value
			eps = dEspArray[EspCount];
			double dCompressRatio, dSegmentRatio, dRMSE, dRunningTime;

			// Run single-stream algorithm for each frequency and threshold
			runAlg(algo, outlier, eps, bucketUpdateFrequenty, dataLoader , dCompressRatio, dSegmentRatio, dRMSE, dRunningTime);

			// Metrics
			dCompressionRatioStaticstic[FreqCount * nNumOfEsp + EspCount] = dCompressRatio;
			dSegmentRatioStaticstic[FreqCount * nNumOfEsp + EspCount] = dSegmentRatio;
			dRMSEStaticstic[FreqCount * nNumOfEsp + EspCount] = dRMSE;
			dTimeStaticstic[FreqCount * nNumOfEsp + EspCount] = dRunningTime;
		}
	}

	// Write statistic information into file
	statistics(data_category, algo, (char*)"CmpRatio", outlier, dCompressionRatioStaticstic, nNumOfEsp, dEspArray , nNumOfFrequency, nFreqArray);
	statistics(data_category, algo, (char*)"SegRatio", outlier, dSegmentRatioStaticstic, nNumOfEsp, dEspArray , nNumOfFrequency, nFreqArray);
	statistics(data_category, algo, (char*)"RMSE", outlier, dRMSEStaticstic, nNumOfEsp, dEspArray , nNumOfFrequency, nFreqArray);
	statistics(data_category, algo, (char*)"Time", outlier, dTimeStaticstic, nNumOfEsp, dEspArray , nNumOfFrequency, nFreqArray);

	// Free staticstic memory
	free(dCompressionRatioStaticstic);
	free(dSegmentRatioStaticstic);
	free(dRMSEStaticstic);
	free(dTimeStaticstic);

	// Free memory
	delete[] data_category;
}

#endif
