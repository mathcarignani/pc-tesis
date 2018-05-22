#include "stdafx.h"
//#include <stdio.h>

// Add ----> A
//#include <crtdbg.h>
// Add <---- A

#include <iostream>
//#include <conio.h>
#include <time.h>
#include "Algorithms/GAMPS/control/GAMPS.h"
#include "Algorithms/APCA/Control/APCA.h"
#include "Algorithms/SlideFilter/Control/SlideFilters.h"
#include "Algorithms/PWLH/Control/PWLH.h"
#include "DataManagementLayer/Dataloader/DataLoader.h"
#include "DataManagementLayer/Data/MultiDataStream.h"
#include "Algorithms/GAMPS/data/GAMPSInput.h"
#include "Algorithms/CHEB/Control/CHEB.h"
#include "Algorithms/PCA/Control/PCA.h"
#include "Config/Config.h"
#include "Config/Config_Reader.h"
#include "Utils/dirent.h"
#include "Utils/file_operation.h"
#include "Utils/KPI_statistics.h"
#include "Experiments/Experiment_Single_Stream.h"
#include "Experiments/Experiment_Multi_Stream.h"
#include <sys/stat.h>
#include <sys/types.h>

//Add ----> A
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif
// Add <---- A

#define DATA_CATEGORY "temp_new"

using namespace std;

void run_no_outlier()
{
	// Add ----> A
	//_CrtSetDbgFlag ( _CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF );
	// Add <---- A

	// Read parameters in the configuration file
	strcpy(Config::pfile, (char*)"/home/xuanluong/Downloads/benchmark/config.ini");
	char* algorithm = new char[200];
	Config::getString((char*)"run",(char*)"algorithm",algorithm);

    //printf(algorithm);
    //printf("\n");

	char** algorithmList = new char*[6];

	char* temp = strtok (algorithm,";");
	int algorithmCount = 0;

	while(temp != NULL)
	{
		algorithmList[algorithmCount++] = temp;
		temp = strtok (NULL,";");
	}

	// Get Epsilon parameter
	int nNumOfEsp = 0;
	double *dEspArray = GetEspArray(nNumOfEsp);

	// Get Update Frequency parameter
	int nNumOfFrequency = 0;
	int *nUpdateFreq = GetUpdateFrequency(nNumOfFrequency);
	for(int i = 0; i < algorithmCount; i++)
	{
		DataLoader* dataLoader = new DataLoader();

		// Multi Stream
		if(!strcmp(strupr(algorithmList[i]), "GAMPS"))
		{
			GAMPS_Alg(nNumOfEsp, dEspArray,nNumOfFrequency,nUpdateFreq, dataLoader);
		}
		// Single Stream
		else
		{
			SingleStream_Alg(algorithmList[i], nNumOfEsp, dEspArray, nNumOfFrequency, nUpdateFreq, dataLoader);
		}

		delete[]dataLoader;

		printf("\n Finish algorithm: %s\n", algorithmList[i]);
	}

	// Free memory local pointer
	delete[] algorithm;
	delete[] algorithmList;
	free(dEspArray);
	free(nUpdateFreq);

	// Free memory for Config class
	Config::FreeMemoryForClass();

	printf("\n---------------------DONE---------------------------");
	//getch();
    std::cin.get();
}

void run_with_outlier()
{
	// Add ----> A
	//_CrtSetDbgFlag ( _CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF );
	// Add <---- A

	// Read parameters
	strcpy(Config::pfile, ".\\config.ini");
	char* algorithm = new char[200];
	Config::getString((char*)"RUN",(char*)"algorithm",algorithm);

	char** algorithmList = new char*[6];
	char* temp = strtok (algorithm,";");
	int algorithmCount = 0;

	while(temp != NULL)
	{
		algorithmList[algorithmCount++] = temp;
		temp = strtok (NULL,";");
	}

	// Get Epsilon parameter
	int nNumOfEsp = 1;
	double *dEspArray = new double(1);
	dEspArray[0] = 0.05;

	// Get Update Frequency parameter
	int nNumOfFrequency = 1;
	int *nUpdateFreq = GetUpdateFrequency(nNumOfFrequency);

	for(int i = 0; i < algorithmCount; i++)
	{
		DataLoader* dataLoader = new DataLoader();

		// Multi Stream
		if(!strcmp(strupr(algorithmList[i]), "GAMPS"))
		{
			GAMPS_Alg(nNumOfEsp, dEspArray,nNumOfFrequency,nUpdateFreq, dataLoader);
		}
		// Single Stream
		else
		{
			SingleStream_Alg(algorithmList[i], nNumOfEsp, dEspArray, nNumOfFrequency, nUpdateFreq, dataLoader);
		}

		delete[]dataLoader;

		printf("\n Finish algorithm: %s", algorithmList[i]);
	}

	// Free memory local pointer
	delete[] algorithm;
	delete[] algorithmList;
	free(dEspArray);
	free(nUpdateFreq);

	// Free memory for Config class
	Config::FreeMemoryForClass();

	printf("\n---------------------DONE---------------------------");
	//getch();
    std::cin.get();
}

int main(){
	run_no_outlier();
    return 0;
}

