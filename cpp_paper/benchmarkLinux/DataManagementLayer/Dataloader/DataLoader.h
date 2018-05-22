#ifndef __DataLoader_H
#define __DataLoader_H

#include "../Data/DataStream.h"

class DataLoader
{
public:
	CDataStream* read_from_File(char* filename,int updateFrequency);
};

#endif