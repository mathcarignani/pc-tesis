#ifndef __SLIDEFILTERS_H
#define __SLIDEFILTERS_H

#include "../../Algo.h"
#include "../../../stdafx.h"
#include "../../../DataStructures/Line/Line.h"
#include "../../../DataManagementLayer/Data/DataStream.h"
#include "../Data/SlideFiltersEntry.h"
#include "../Data/SlideFiltersOutPut.h"

class SlideFilters : public Algo
{
private:
	SlideFiltersOutput* m_pSFOutput;
	SlideFiltersInput* m_pSFData;

	int m_nBegin_Point;

	Line m_curU;// Upper bound line
	Line m_curL;// Lower bound line
	Line m_curG;// Current segment
	Line m_prevG;// Previous segment

	// Initialize upper bound and lower bound
	void initializeU_L(double beg_ts, double beg_v, double end_ts, double end_v, double eps);

	// Update upper bound and lower bound
	bool updateUandLforConnectedSegment(Line& curU, Line& curL, Line prevG);

	// Find the fittest line in range of lower bound and upper bound
	Line getFittestLine_G(int beginPoint, int endPoint, Line curU, Line curL);

	// Generate line segments for the filtering intervals and update the latest-executed point
	void recording_mechanism(int& position);

	// Adjust upper bound and lower bound with the arrival of each new data point at 'position'
	void filtering_mechanism(int position);

public:
	SlideFilters(SlideFiltersInput* data);
	~SlideFilters();

	SlideFiltersOutput* getOutput();
	virtual void compress();
};

#endif
