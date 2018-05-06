#ifndef __APCA_H
#define __APCA_H

#include "../../Algo.h"
#include "../Data/APCAOutput.h"
#include "../Data/APCAInput.h"
#include "../../../DataManagementLayer/Data/DataStream.h"

class APCA : public Algo
{
private:
	APCAInput*  m_pInput;
	APCAOutput* m_pOutput;

public:
	APCA(APCAInput*);
	~APCA(void);

	virtual Output* getOutput();
	virtual void compress();// Compute model parameters
};

#endif


