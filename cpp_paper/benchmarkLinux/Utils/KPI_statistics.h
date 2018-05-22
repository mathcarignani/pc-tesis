#ifndef __KPI_STATISTICS_H
#define __KPI_STATISTICS_H

//#include <windows.h>
#include <string.h>
#include <assert.h>
#include <sys/stat.h>

// Write statistics information for a given frequency and threshold
static void writeKPI(char* filename, char* data_category, char* alg, char* metric, double outlier, double threshold, double frequency, double value)
{
	FILE *file = fopen(filename, "a");
	char temp[100];
	::memset(temp, 0, sizeof(char) * 100);

	if (file == NULL) perror ("Error opening file");
	else
	{
		char tuple[1000];
		::memset(tuple, 0, sizeof(char) * 1000);
		::strcat(tuple, data_category);
		::strcat(tuple, ",");
		::strcat(tuple, alg);
		::strcat(tuple, ",");
		::strcat(tuple, metric);

		::strcat(tuple, ",");
		::sprintf(temp, "%.5f", outlier);
		::strcat(tuple, temp);

		::strcat(tuple, ",");
		::sprintf(temp, "%.5f", threshold);
		::strcat(tuple, temp);

		::strcat(tuple, ",");
		::sprintf(temp, "%.5f", frequency);
		::strcat(tuple, temp);

		::strcat(tuple, ",");
		::sprintf(temp, "%.10f", value);
		::strcat(tuple, temp);

		fputs(tuple, file);
		fputs("\n", file);
		fclose (file);
	}
}

// Write statistics information for all frequencies and thresholds
static void writeStatistics(char* filePath, char* data_category, char* alg, char* metric, double outlier, double *dStatistics, int nNumOfEps, double* dEpsArray, int nNumOfFreq, int *nFreqArray)
{
	FILE *file = fopen(filePath, "w");
	char cFrequence[300];
	char cEpsilon[300];

	if (file == NULL) perror ("Error opening file");
	else
	{
		for(int i = 0; i < nNumOfFreq; i++)
		{
			char temp[200];
			::memset(temp, 0, sizeof(char) * 10);
			::memset(cFrequence, 0, sizeof(char) * 300);

			// Frequency line
			::strcat(cFrequence, "+ Frequency = ");
			::itoa(nFreqArray[i], temp, 200);
			::strcat(cFrequence, temp);
			::strcat(cFrequence, " :\n");
			fputs(cFrequence, file);

			for(int j = 0; j < nNumOfEps; j++)
			{
				// Write statistics information
				writeKPI((char*)"statistic_KPI.csv", data_category, alg, metric, outlier, dEpsArray[j], nFreqArray[i], dStatistics[i * nNumOfEps + j]);

				::memset(cEpsilon, 0, sizeof(char) * 300);
				::memset(temp, 0, sizeof(char) * 200);

				// Epsilon line
				::strcat(cEpsilon, "\t - Epsilon = ");
				::sprintf(temp, "%.3f : \t", dEpsArray[j]);
				::strcat(cEpsilon, temp);
				::memset(temp, 0, sizeof(char) * 200);
				::sprintf(temp, "%.10f \n", dStatistics[i * nNumOfEps + j]);
				::strcat(cEpsilon, temp);
				fputs(cEpsilon, file);
			}

			fputs("\n", file);
		}
		fclose (file);
	}
}

#endif
