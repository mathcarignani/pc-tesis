#include "../../stdafx.h"
#include "DataLoader.h"

char* delimiters = (char*)",";

CDataStream* DataLoader::read_from_File(char *filename,int updateFrequency)
{
    //printf("%s\n",filename);
    //printf("%d\n",updateFrequency);
	FILE *file = fopen(filename, "r");
	CDataStream* dataStream = new CDataStream();
	char* buffer = new char[50];

	// Read original update frequency
	if (!feof (file) )
	{
		fgets (buffer, 50, file);
		int j=0;
		while(buffer[j] != 0)
		{
			buffer[j] = buffer[j+3];
			++j;
		}
	}
    //printf("%s\n",buffer);
	int rate = atoi(buffer);
    //printf("%d\n",rate);
	// Normalize update frequency
	updateFrequency = updateFrequency / rate;
    //printf("%d\n",updateFrequency);
    //printf("%d\n",rate);

	if (updateFrequency == 0){
		updateFrequency = 1;
	}
	updateFrequency = 1;

	int timestamp = 0;
	if (file == NULL)
	{
		perror ("Error opening file");
	}
	else
	{
		if (updateFrequency == 0)
		{
			fclose (file);
			delete[] buffer;
			return dataStream;
		}

		int i = updateFrequency - 1;//to get first point
		int count =0;
		while ( !feof (file) )
		{
			//Read line by line
			buffer[0] = '\0';
			fgets (buffer, 50, file);
			if (buffer[0] == '\0') continue;
			if (++i != updateFrequency) continue;
			i = 0;
			timestamp++;
			double value = atof(buffer);
			if (value > 10000 || value < -10000)
			{
				printf("%s",filename);
                printf(" dataloader: value > 10000 || value < -10000");
                printf("\n");
				break;
			}

			//Add entry to data stream
			DataItem entry;
			entry.value = value;
			entry.timestamp = timestamp;
            //printf("Value %f. Timestamp %d.\n",value,timestamp);
			dataStream->add(entry);

			count++;
			if (count > 5000)
				break;
		}

		fclose (file);
	}
	dataStream->statistic();

	delete[] buffer;
	return dataStream;
}
