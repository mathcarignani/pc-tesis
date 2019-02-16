#ifndef __GAMPS_COMPUTATION_CPP
#define __GAMPS_COMPUTATION_CPP

#include "../../../stdafx.h"
#include "FacilityLocProb.h"
#include "../../../DataManagementLayer/Data/DataStream.h"
#include "GAMPS_Computation.h"

GAMPS_Computation::GAMPS_Computation(GAMPSInput* gampsInput,double eps)
{
	m_pInput = gampsInput;
	m_dEps = eps;
	m_pGampsOutput = new GAMPSOutput(gampsInput);
}

GAMPS_Computation::~GAMPS_Computation()
{
	delete m_pGampsOutput;
}

// static group current input data
int GAMPS_Computation::statGroup()
{
	return statGroup(this->m_pInput);
}

GAMPSOutput* GAMPS_Computation::getGampsOutput()
{
	return this->m_pGampsOutput;
}

// duplicate original data
CMultiDataStream* GAMPS_Computation::copyDataToTemp(CMultiDataStream* original)
{
	int numOfStream = original->getNumOfStream();
	CMultiDataStream* tempData = new CMultiDataStream(numOfStream);
	for(int i = 0; i < numOfStream; i++)
	{
		CDataStream* retrieve = original->getDataAt(i);
		CDataStream* temp = new CDataStream(*retrieve);
		tempData->addSingleStream(temp);
	}
	return tempData;
}

// Purpose	: calculate error tolerance for ratio signal
// Parameter:
//            eps1: epsilon 1 which used to compress base signal by APCA
//            c1: max ratio value
//            c2: max value of base signal
double GAMPS_Computation::computeEps2(double eps1, double c1, double c2)
{
	double eps2 = this->m_dEps - c1 * eps1;
	eps2 = eps2 / (c2 + eps1);
	return eps2;
}

// Purpose	: apply APCA to compress original data with maximum error tolerance
// Parameter:
//            stream: data need to compress
//            eps: maximum error tolerance - epsilon
DynArray<GAMPSEntry>* GAMPS_Computation::compress_APCA(CDataStream* stream, double esp)
{
	DynArray<GAMPSEntry>* compressData = new DynArray<GAMPSEntry>();
	double doubleEsp = 2* esp;
	double currentMax = 0;
	double currentMin = 0;
	int inputCount = stream->size();

	if( inputCount <= 0) return compressData;
	DataItem item = stream->getAt(0);
	currentMax = item.value;
	currentMin= item.value;

	for(int i = 0; i< inputCount;i++)
	{
		double tempMax  = currentMax;
		double tempMin  = currentMin;
		DataItem item = stream->getAt(i);
		double newValue = item.value;

		if(currentMax < newValue)
			tempMax = newValue;

		if(currentMin > newValue)
			tempMin = newValue;

		if((tempMax - tempMin) > doubleEsp)
		{
			GAMPSEntry compress;
			compress.value = (currentMax+ currentMin)/2;
			compress.endingTimestamp = item.timestamp - 1;
			currentMax = newValue;
			currentMin= newValue;
			compressData-> add(compress);
		}
		else
		{
			currentMax = tempMax;
			currentMin = tempMin;
		}
	}

	//add the last point
	GAMPSEntry entry;
	entry.value = (currentMax + currentMin) / 2;
	entry.endingTimestamp = inputCount;
	compressData->add(entry);

	return compressData;
}

// Purpose	: apply APCA to compress ratio signal with maximum error tolerance
// Parameter:
//            computeRatioList: ratio signal to compress
//            eps: maximum error tolerance - epsilon
DynArray<GAMPSEntry>* GAMPS_Computation::compress_APCA(DynArray<GAMPSEntry>& computeRatioList, double esp)
{
	DynArray<GAMPSEntry>* compressData = new DynArray<GAMPSEntry>();
	double doubleEsp = 2* esp;
	double currentMax, currentMin = 0;

	int inputCount = computeRatioList.size();
	if(inputCount <= 0)	return compressData;

	GAMPSEntry item = computeRatioList.getAt(0);
	currentMax = item.value;
	currentMin= item.value;

	for(int i = 0; i< inputCount;i++)
	{
		double tempMax  = currentMax;
		double tempMin  = currentMin;
		GAMPSEntry item = computeRatioList.getAt(i);
		double newValue = item.value;

		if(currentMax < newValue)
			tempMax = newValue;

		if(currentMin > newValue)
			tempMin = newValue;

		if((tempMax - tempMin) > doubleEsp)
		{
			GAMPSEntry compress;
			compress.value = (currentMax+ currentMin)/2;
			compress.endingTimestamp = item.endingTimestamp - 1;
			currentMax = newValue;
			currentMin= newValue;
			compressData-> add(compress);
		}
		else
		{
			currentMax = tempMax;
			currentMin = tempMin;
		}
	}

	//add the last point
	GAMPSEntry entry;
	entry.value = (currentMax + currentMin) / 2;
	entry.endingTimestamp = inputCount;
	compressData->add(entry);

	return compressData;
}

// Purpose	: given original signal, calculate its ratio signal with respect to base signal
// Parameter:
//          (In):
//            computeSignal: signal need to compute ratio with base signal
//            baseSignal:base signal
//          (Out):
//            c1: max ratio value
//            c2: max value of base signal
// Return	: (DynArray<GAMPSEntry>*)pointer to ratio signal data
DynArray<GAMPSEntry>* GAMPS_Computation::computeRatioSignal(CDataStream* computeSignal,CDataStream* baseSignal,double& c1, double& c2)
{
	double maxC1,maxC2;
	DynArray<GAMPSEntry>* listRatioSignal = new DynArray<GAMPSEntry>();
	int baseSignalSize = baseSignal->size();

	if(baseSignalSize > 0)
	{
		DataItem baseEntry = baseSignal->getAt(0);
		DataItem computeEntry = computeSignal->getAt(0);
		if (baseEntry.value < 1 && baseEntry.value > -1)
			baseEntry.value =1;

		double ratioValue = computeEntry.value / baseEntry.value;
		GAMPSEntry ratioEntry;
		ratioEntry.value = ratioValue;
		ratioEntry.endingTimestamp = baseEntry.timestamp;
		listRatioSignal->add(ratioEntry);
		maxC1 = ratioValue;
		maxC2 = baseEntry.value;
	}

	for(int i = 1; i < baseSignalSize; i++)
	{
		DataItem baseEntry = baseSignal->getAt(i);
		DataItem computeEntry = computeSignal->getAt(i);

		// in case of baseEntry.value == 0
		if (baseEntry.value < 1 && baseEntry.value > -1)
			baseEntry.value =1;

		double ratioValue = computeEntry.value / baseEntry.value;

		GAMPSEntry ratioEntry;
		ratioEntry.value = ratioValue;
		ratioEntry.endingTimestamp = baseEntry.timestamp;
		listRatioSignal->add(ratioEntry);

		if(ratioValue > maxC1)
			maxC1 = ratioValue;

		if(baseEntry.value > maxC2)
			maxC2 = baseEntry.value;
	}

	c1 = maxC1;
	c2 = maxC2;

	return listRatioSignal;
}

// Purpose	: static group given input data
// Parameter:
//            gampsInputList: data need to be static grouped
// Return	: (int)allocated memory of stat grouped result
int GAMPS_Computation::statGroup(GAMPSInput* gampsInputList)
{
	// init
	int numOfStream = gampsInputList->getNumOfStream();
	DynArray<GAMPSEntry>** listBucket = new DynArray<GAMPSEntry>*[numOfStream];
	DynArray<GAMPSEntry>** listRatioSignalBucket = new DynArray<GAMPSEntry>*[numOfStream*numOfStream];
	double eps = 0;
	double eps1 = 0;
	double eps2 = 0;

	// Apply APCA
	for(int j = 0; j< numOfStream;j++)
	{
		// choose one signal => base signal, compress it and push into base signal bucket list
		CDataStream* baseSignal = gampsInputList->getOriginalStreams()->getDataAt(j);

		// calculate % eps
		baseSignal->statistic();
		eps = m_dEps * (baseSignal->getMax() - baseSignal->getMin());
		eps1 = 0.4 * eps;

		DynArray<GAMPSEntry>* listBaseSignalBucket = compress_APCA(baseSignal,eps1);
		listBucket[j] = listBaseSignalBucket;

		for(int i = 0; i < numOfStream; i++)
		{
			/*
			foreach signal:
				+ calculate ratio with base signal
				+ apply APCA and push it into ratio bucket list
			*/
			CDataStream* ratioSignal = gampsInputList->getOriginalStreams()->getDataAt(i);
			double c1,c2;
			DynArray<GAMPSEntry> *listComputeRatioSignal = this->computeRatioSignal(ratioSignal,baseSignal,c1,c2);

			eps2 = this->computeEps2(eps1,c1,c2);
			DynArray<GAMPSEntry> *listRatioBucket = this->compress_APCA(*listComputeRatioSignal,eps2);
			int pos = j* numOfStream + i;
			listRatioSignalBucket[pos] = listRatioBucket;
			delete listComputeRatioSignal;
		}
	}

	/*************** facility location *************/
	int bSize = numOfStream;
	int* baseBucketCost = new int[numOfStream];
	DynArray<int>** ratioSignalCost= new DynArray<int>*[numOfStream];

	// calculate each base signal bucket cost
	for(int i = 0; i < bSize; i++)
	{
		int oneBSize = listBucket[i]->size();
		baseBucketCost[i] = oneBSize;
	}

	// put ratio signal cost into 2 dimension array array[baseSignal][ratioSignal]
	for(int i = 0; i < bSize; i++)
	{
		DynArray<int>* tempArray = new DynArray<int>();
		for(int j = 0; j< bSize; j++)
		{
			if(i != j)
			{
				int temp = 0;
				int pos = i * bSize + j;
				int oneSSize = listRatioSignalBucket[pos]->size();
				tempArray->add(oneSSize);
			}
			else
			{
				int bucketSize = baseBucketCost[i];
				tempArray->add(bucketSize);
			}
		}
		ratioSignalCost[i] = tempArray;
	}

	FacilityLocProb* facilityPro = new FacilityLocProb(numOfStream);
	facilityPro->setArrBaseCost(baseBucketCost);
	facilityPro->setRatioCost(ratioSignalCost);

	// find optimal solution for faciliting location
	int totalCost = facilityPro->findOptimalSolution();
	m_pGampsOutput->setTgood(facilityPro->getTgood());
	m_pGampsOutput->setTgoodSize(numOfStream);
	computeOutput(listBucket,listRatioSignalBucket);
	/************ end facility location ************/

	// deallocate memory
	delete facilityPro;
	for(int j = 0; j < bSize;j++)
	{
		delete ratioSignalCost[j];
		delete listBucket[j];
		for(int i = 0; i < bSize; i++)
		{
			int pos = j* numOfStream + i;
			delete listRatioSignalBucket[pos];
		}
	}
	delete[] ratioSignalCost;
	delete baseBucketCost;
	delete[] listBucket;
	delete[] listRatioSignalBucket;

	return totalCost;
}

// compute output based on base signals and ratio signals
void GAMPS_Computation:: computeOutput(DynArray<GAMPSEntry>** baseBucketList, DynArray<GAMPSEntry>** ratioBucketList)
{
	int numOfStream = this->m_pInput->getNumOfStream();
	int baseBucketCount = 0;
	int baseCount = 0;
	int ratioCount = 0;

	for(int i = 0; i < numOfStream; i++)
	{
		if(m_pGampsOutput->getTgood()[i] == i)
			baseBucketCount++;
	}

	DynArray<GAMPSEntry>** resultBaseSignal =  new DynArray<GAMPSEntry>*[baseBucketCount];
	DynArray<GAMPSEntry>** resultRatioSignal;

	if(baseBucketCount < numOfStream)
		resultRatioSignal = new DynArray<GAMPSEntry>*[numOfStream - baseBucketCount];

	for(int i = 0; i < numOfStream; i++)
	{
		if(m_pGampsOutput->getTgood()[i] == i)
		{
			DynArray<GAMPSEntry>* temp = new DynArray<GAMPSEntry>(*baseBucketList[i]);
			resultBaseSignal[baseCount++] = temp;
		}
		else
		{
			int pos = m_pGampsOutput->getTgood()[i] * numOfStream + i;
			DynArray<GAMPSEntry>* temp = new DynArray<GAMPSEntry>(*ratioBucketList[pos]);
			resultRatioSignal[ratioCount++] =  temp;
		}
	}

	std::cout << "baseCount = " << baseCount << std::endl;
	std::cout << "ratioCount = " << ratioCount << std::endl;

	m_pGampsOutput->setResultBaseSignal(resultBaseSignal);
	m_pGampsOutput->setResultRatioSignal(resultRatioSignal);
}

void GAMPS_Computation::print(DynArray<GAMPSEntry>* array, int spaces){
    int inputCount = array->size();
    for (int i=0; i < inputCount; i++){
        GAMPSEntry baseEntry = array->getAt(i);
        for(int j=0; j < spaces; j++) { std::cout << "    "; }
        std::cout << "ts = " << baseEntry.endingTimestamp << ", val = " << baseEntry.value << std::endl;
    }
}

#endif
